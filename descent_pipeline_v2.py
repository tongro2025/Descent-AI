#!/usr/bin/env python3
"""
Descent Pipeline - 우승 레벨 개선 버전
P0: 드라이런 + 아이도포턴시 + 에러 처리
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import yaml
from google.cloud import bigquery
from google.api_core import retry, exceptions
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PipelineConfig:
    """파이프라인 설정"""
    project_id: str
    dataset_id: str
    location: str = "US"
    mode: str = "vertex"  # vertex, oss, native
    dry_run: bool = False
    max_retries: int = 3
    retry_delay: float = 1.0
    ori_weight: float = 0.7
    ori_threshold: float = 0.3
    top_k: int = 10
    enable_incremental: bool = True
    enable_cost_logging: bool = True

class PipelineRunner:
    """파이프라인 실행기"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.client = bigquery.Client(project=config.project_id)
        self.run_log = []
        self.cost_log = []
        
    def log_step(self, step: str, status: str, details: Dict[str, Any] = None):
        """단계 로깅"""
        log_entry = {
            "timestamp": time.time(),
            "step": step,
            "status": status,
            "details": details or {}
        }
        self.run_log.append(log_entry)
        logger.info(f"[{status.upper()}] {step}: {details}")
        
    def log_cost(self, job_id: str, step: str):
        """비용 로깅"""
        if not self.config.enable_cost_logging:
            return
            
        try:
            job = self.client.get_job(job_id)
            stats = job.statistics
            
            cost_entry = {
                "timestamp": time.time(),
                "step": step,
                "job_id": job_id,
                "slot_ms": getattr(stats, 'total_slot_ms', 0),
                "bytes_processed": getattr(stats.query, 'total_bytes_processed', 0) if hasattr(stats, 'query') else 0,
                "creation_time": job.created.isoformat() if job.created else None,
                "end_time": job.ended.isoformat() if job.ended else None
            }
            self.cost_log.append(cost_entry)
        except Exception as e:
            logger.warning(f"비용 로깅 실패: {e}")
    
    @retry.Retry(
        predicate=retry.if_exception_type(exceptions.ServiceUnavailable, exceptions.InternalServerError),
        deadline=300.0,
        initial=1.0,
        maximum=60.0,
        multiplier=2.0
    )
    def execute_query(self, sql: str, step: str, dry_run: bool = None) -> Optional[str]:
        """쿼리 실행 (리트라이 포함)"""
        if dry_run is None:
            dry_run = self.config.dry_run
            
        if dry_run:
            logger.info(f"[DRY_RUN] {step}: {sql[:100]}...")
            return None
            
        try:
            job_config = bigquery.QueryJobConfig(dry_run=dry_run)
            job = self.client.query(sql, job_config=job_config)
            
            if not dry_run:
                job.result()  # Wait for completion
                self.log_cost(job.job_id, step)
                self.log_step(step, "SUCCESS", {"job_id": job.job_id})
                return job.job_id
            else:
                self.log_step(step, "DRY_RUN", {"estimated_bytes": job.total_bytes_processed})
                return None
                
        except Exception as e:
            self.log_step(step, "ERROR", {"error": str(e)})
            raise
    
    def add_content_hash(self):
        """콘텐츠 해시 추가 (아이도포턴시)"""
        step = "add_content_hash"
        sql = f"""
        ALTER TABLE `{self.config.project_id}.{self.config.dataset_id}.raw_texts`
        ADD COLUMN IF NOT EXISTS content_hash INT64;
        
        UPDATE `{self.config.project_id}.{self.config.dataset_id}.raw_texts`
        SET content_hash = FARM_FINGERPRINT(CONCAT(body))
        WHERE content_hash IS NULL;
        """
        
        self.execute_query(sql, step)
    
    def create_ori_params_table(self):
        """ORI 파라미터 테이블 생성"""
        step = "create_ori_params"
        sql = f"""
        CREATE OR REPLACE TABLE `{self.config.project_id}.{self.config.dataset_id}.ori_params` AS
        SELECT 
            {self.config.ori_weight} AS w,
            {self.config.ori_threshold} AS tau,
            {self.config.top_k} AS top_k,
            '{self.config.mode}' AS mode;
        """
        
        self.execute_query(sql, step)
    
    def incremental_text_embedding(self):
        """증분 텍스트 임베딩"""
        step = "incremental_text_embedding"
        
        if self.config.mode == "vertex":
            # Vertex AI 기반 증분 임베딩
            sql = f"""
            CREATE OR REPLACE TABLE `{self.config.project_id}.{self.config.dataset_id}.emb_text_new` AS
            SELECT t.id, t.body, t.content_hash
            FROM `{self.config.project_id}.{self.config.dataset_id}.raw_texts` t
            LEFT JOIN `{self.config.project_id}.{self.config.dataset_id}.emb_view_t_vertex` e USING(id)
            WHERE e.id IS NULL;
            
            -- 새로 생성된 임베딩을 기존 테이블에 MERGE
            MERGE `{self.config.project_id}.{self.config.dataset_id}.emb_view_t_vertex` AS target
            USING `{self.config.project_id}.{self.config.dataset_id}.emb_text_new` AS source
            ON target.id = source.id
            WHEN NOT MATCHED THEN
            INSERT (id, embedding) VALUES (source.id, 
                -- 여기서 실제 Vertex AI 호출 (Python에서 처리)
                [0.0]  -- 플레이스홀더
            );
            """
        else:
            # OSS 기반 증분 임베딩
            sql = f"""
            CREATE OR REPLACE TABLE `{self.config.project_id}.{self.config.dataset_id}.emb_text_new` AS
            SELECT t.id, t.body, t.content_hash
            FROM `{self.config.project_id}.{self.config.dataset_id}.raw_texts` t
            LEFT JOIN `{self.config.project_id}.{self.config.dataset_id}.emb_view_t` e USING(id)
            WHERE e.id IS NULL;
            """
        
        self.execute_query(sql, step)
    
    def create_evaluation_harness(self):
        """평가 하니스 생성"""
        step = "create_evaluation_harness"
        sql = f"""
        CREATE OR REPLACE VIEW `{self.config.project_id}.{self.config.dataset_id}.eval_metrics` AS
        WITH labels AS (
            SELECT 'A100' id, 1 y UNION ALL
            SELECT 'A200', 1 UNION ALL
            SELECT 'A300', 1 UNION ALL
            SELECT 'B100', 0 UNION ALL
            SELECT 'B200', 0 UNION ALL
            SELECT 'C100', 0
        ),
        predictions AS (
            SELECT id, predict FROM `{self.config.project_id}.{self.config.dataset_id}.report_ori`
        ),
        metrics AS (
            SELECT 
                COUNT(*) as total_cases,
                SUM(CASE WHEN p.predict = l.y THEN 1 ELSE 0 END) as correct_predictions,
                AVG(CASE WHEN p.predict = l.y THEN 1.0 ELSE 0.0 END) as accuracy,
                -- Precision@K 계산
                SUM(CASE WHEN p.predict = 1 AND l.y = 1 THEN 1 ELSE 0 END) as true_positives,
                SUM(CASE WHEN p.predict = 1 THEN 1 ELSE 0 END) as predicted_positives,
                SUM(CASE WHEN l.y = 1 THEN 1 ELSE 0 END) as actual_positives
            FROM predictions p
            LEFT JOIN labels l ON p.id = l.id
        )
        SELECT 
            total_cases,
            correct_predictions,
            accuracy,
            ROUND(accuracy * 100, 2) as accuracy_percent,
            SAFE_DIVIDE(true_positives, predicted_positives) as precision,
            SAFE_DIVIDE(true_positives, actual_positives) as recall,
            SAFE_DIVIDE(2 * true_positives, predicted_positives + actual_positives) as f1_score
        FROM metrics;
        """
        
        self.execute_query(sql, step)
    
    def save_artifacts(self):
        """아티팩트 저장"""
        artifacts_dir = Path("artifacts")
        artifacts_dir.mkdir(exist_ok=True)
        
        # 실행 로그 저장
        with open(artifacts_dir / "run_log.jsonl", "w") as f:
            for entry in self.run_log:
                f.write(json.dumps(entry) + "\n")
        
        # 비용 로그 저장
        if self.cost_log:
            with open(artifacts_dir / "cost_report.csv", "w") as f:
                f.write("timestamp,step,job_id,slot_ms,bytes_processed,creation_time,end_time\n")
                for entry in self.cost_log:
                    f.write(f"{entry['timestamp']},{entry['step']},{entry['job_id']},{entry['slot_ms']},{entry['bytes_processed']},{entry['creation_time']},{entry['end_time']}\n")
        
        logger.info(f"아티팩트 저장 완료: {artifacts_dir}")
    
    def run_pipeline(self):
        """전체 파이프라인 실행"""
        logger.info(f"파이프라인 시작: {self.config.mode} 모드, 드라이런: {self.config.dry_run}")
        
        try:
            # P0: 아이도포턴시
            self.add_content_hash()
            
            # P0: ORI 파라미터 외부화
            self.create_ori_params_table()
            
            # P1: 증분 임베딩
            if self.config.enable_incremental:
                self.incremental_text_embedding()
            
            # P2: 평가 하니스
            self.create_evaluation_harness()
            
            # 아티팩트 저장
            self.save_artifacts()
            
            logger.info("파이프라인 완료!")
            
        except Exception as e:
            logger.error(f"파이프라인 실패: {e}")
            self.save_artifacts()
            raise

def load_config(config_path: str = "config.yaml") -> PipelineConfig:
    """설정 파일 로드"""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # 환경변수 치환 처리
        if 'project_id' in config_data:
            project_id = config_data['project_id']
            if project_id.startswith('${') and project_id.endswith('}'):
                # ${GCP_PROJECT_ID:-your-project-id} 형태 처리
                env_var = project_id[2:-1]  # GCP_PROJECT_ID:-your-project-id
                if ':-' in env_var:
                    var_name, default_value = env_var.split(':-', 1)
                    config_data['project_id'] = os.getenv(var_name, default_value)
                else:
                    config_data['project_id'] = os.getenv(env_var, project_id)
        
        return PipelineConfig(**config_data)
    else:
        # 기본 설정 생성
        from dotenv import load_dotenv
        load_dotenv()
        
        config = PipelineConfig(
            project_id=os.getenv("GCP_PROJECT", "your-project-id"),
            dataset_id=os.getenv("BQ_DATASET", "descent_demo"),
            location=os.getenv("BQ_LOCATION", "US"),
            mode=os.getenv("DESCENT_MODE", "vertex")
        )
        
        # 설정 파일 저장
        with open(config_path, 'w') as f:
            yaml.dump(config.__dict__, f, default_flow_style=False)
        
        return config

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Descent Pipeline - 우승 레벨")
    parser.add_argument("--config", default="config.yaml", help="설정 파일 경로")
    parser.add_argument("--dry-run", action="store_true", help="드라이런 모드")
    parser.add_argument("--mode", choices=["vertex", "oss", "native"], help="실행 모드")
    
    args = parser.parse_args()
    
    config = load_config(args.config)
    if args.dry_run:
        config.dry_run = True
    if args.mode:
        config.mode = args.mode
    
    runner = PipelineRunner(config)
    runner.run_pipeline()
