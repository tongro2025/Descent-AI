#!/usr/bin/env python3
"""
Descent CLI - 우승 레벨 명령줄 인터페이스
P3: 코드·CI/CD·가독성
"""

import typer
import yaml
import json
from pathlib import Path
from typing import Optional, List
import subprocess
import sys
from descent_pipeline_v2 import PipelineRunner, PipelineConfig, load_config
from eval_harness import DescentEvaluator

app = typer.Typer(help="Descent Pipeline CLI - Championship Level")

@app.command()
def init(
    project_id: str = typer.Option(..., help="GCP Project ID"),
    dataset_id: str = typer.Option("descent_demo", help="BigQuery Dataset ID"),
    location: str = typer.Option("US", help="BigQuery Region"),
    mode: str = typer.Option("vertex", help="Execution mode (vertex/oss/native)"),
    config_file: str = typer.Option("config.yaml", help="Configuration file path")
):
    """Initialize project"""
    typer.echo(f"🚀 Initializing Descent project: {project_id}.{dataset_id}")
    
    config = PipelineConfig(
        project_id=project_id,
        dataset_id=dataset_id,
        location=location,
        mode=mode
    )
    
    # Save configuration file
    with open(config_file, 'w') as f:
        yaml.dump(config.__dict__, f, default_flow_style=False)
    
    typer.echo(f"✅ Configuration file created: {config_file}")
    
    # Create basic directories
    Path("artifacts").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    typer.echo("✅ Project structure created successfully")

@app.command()
def embed(
    config_file: str = typer.Option("config.yaml", help="Configuration file path"),
    dry_run: bool = typer.Option(False, help="Dry run mode"),
    incremental: bool = typer.Option(True, help="Use incremental embedding")
):
    """Generate embeddings"""
    typer.echo("🧠 Starting embedding generation")
    
    config = load_config(config_file)
    config.dry_run = dry_run
    config.enable_incremental = incremental
    
    runner = PipelineRunner(config)
    
    try:
        runner.run_pipeline()
        typer.echo("✅ Embedding generation completed")
    except Exception as e:
        typer.echo(f"❌ Embedding generation failed: {e}")
        raise typer.Exit(1)

@app.command()
def stitch(
    config_file: str = typer.Option("config.yaml", help="설정 파일 경로"),
    dry_run: bool = typer.Option(False, help="드라이런 모드")
):
    """멀티모달 스티칭"""
    typer.echo("🔗 멀티모달 스티칭 시작")
    
    config = load_config(config_file)
    config.dry_run = dry_run
    
    runner = PipelineRunner(config)
    
    # 스티칭만 실행
    runner.add_content_hash()
    runner.create_ori_params_table()
    
    typer.echo("✅ 스티칭 완료")

@app.command()
def ori(
    config_file: str = typer.Option("config.yaml", help="설정 파일 경로"),
    weight: float = typer.Option(0.7, help="ORI 가중치"),
    threshold: float = typer.Option(0.3, help="ORI 임계값"),
    dry_run: bool = typer.Option(False, help="드라이런 모드")
):
    """ORI 분석 실행"""
    typer.echo("🎯 ORI 분석 시작")
    
    config = load_config(config_file)
    config.ori_weight = weight
    config.ori_threshold = threshold
    config.dry_run = dry_run
    
    runner = PipelineRunner(config)
    
    try:
        runner.create_ori_params_table()
        runner.create_evaluation_harness()
        typer.echo("✅ ORI 분석 완료")
    except Exception as e:
        typer.echo(f"❌ ORI 분석 실패: {e}")
        raise typer.Exit(1)

@app.command()
def report(
    config_file: str = typer.Option("config.yaml", help="설정 파일 경로"),
    modes: List[str] = typer.Option(["text", "multimodal", "native"], help="평가할 모드들"),
    output_format: str = typer.Option("markdown", help="출력 형식 (markdown/json/csv)")
):
    """평가 리포트 생성"""
    typer.echo("📊 평가 리포트 생성 시작")
    
    config = load_config(config_file)
    
    evaluator = DescentEvaluator(config.project_id, config.dataset_id)
    
    try:
        # 모드별 비교
        comparison_df = evaluator.compare_modes(modes)
        
        # 리포트 생성
        report = evaluator.generate_report(comparison_df)
        
        # 결과 저장
        evaluator.save_results(comparison_df, report)
        
        # 출력 형식에 따른 결과 표시
        if output_format == "markdown":
            typer.echo("\n" + report)
        elif output_format == "json":
            results_dict = comparison_df.to_dict('records')
            typer.echo(json.dumps(results_dict, indent=2, ensure_ascii=False))
        elif output_format == "csv":
            typer.echo(comparison_df.to_csv(index=False))
        
        typer.echo("✅ 리포트 생성 완료")
        
    except Exception as e:
        typer.echo(f"❌ 리포트 생성 실패: {e}")
        raise typer.Exit(1)

@app.command()
def test(
    config_file: str = typer.Option("config.yaml", help="설정 파일 경로"),
    test_mode: str = typer.Option("mini", help="테스트 모드 (mini/full)")
):
    """통합 테스트 실행"""
    typer.echo("🧪 통합 테스트 시작")
    
    config = load_config(config_file)
    
    if test_mode == "mini":
        # 미니 테스트: OSS 모드로 빠른 검증
        config.mode = "oss"
        config.dry_run = True
        
        runner = PipelineRunner(config)
        
        try:
            runner.run_pipeline()
            typer.echo("✅ 미니 테스트 통과")
        except Exception as e:
            typer.echo(f"❌ 미니 테스트 실패: {e}")
            raise typer.Exit(1)
    
    elif test_mode == "full":
        # 전체 테스트: 모든 모드 검증
        modes = ["text", "multimodal", "native"]
        
        for mode in modes:
            typer.echo(f"🔍 {mode} 모드 테스트 중...")
            config.mode = mode
            config.dry_run = True
            
            runner = PipelineRunner(config)
            
            try:
                runner.run_pipeline()
                typer.echo(f"✅ {mode} 모드 테스트 통과")
            except Exception as e:
                typer.echo(f"❌ {mode} 모드 테스트 실패: {e}")
                raise typer.Exit(1)
        
        typer.echo("✅ 전체 테스트 통과")

@app.command()
def clean(
    config_file: str = typer.Option("config.yaml", help="설정 파일 경로"),
    artifacts: bool = typer.Option(True, help="아티팩트 삭제"),
    logs: bool = typer.Option(True, help="로그 삭제"),
    tables: bool = typer.Option(False, help="BigQuery 테이블 삭제 (주의!)")
):
    """정리 작업"""
    typer.echo("🧹 정리 작업 시작")
    
    if artifacts:
        import shutil
        if Path("artifacts").exists():
            shutil.rmtree("artifacts")
            typer.echo("✅ 아티팩트 삭제 완료")
    
    if logs:
        import shutil
        if Path("logs").exists():
            shutil.rmtree("logs")
            typer.echo("✅ 로그 삭제 완료")
    
    if tables:
        if typer.confirm("⚠️  BigQuery 테이블을 삭제하시겠습니까?"):
            config = load_config(config_file)
            client = bigquery.Client(project=config.project_id)
            
            # 테이블 목록 가져오기
            tables = client.list_tables(config.dataset_id)
            
            for table in tables:
                client.delete_table(f"{config.project_id}.{config.dataset_id}.{table.table_id}")
                typer.echo(f"✅ 테이블 삭제: {table.table_id}")
    
    typer.echo("✅ 정리 작업 완료")

@app.command()
def status(
    config_file: str = typer.Option("config.yaml", help="설정 파일 경로")
):
    """시스템 상태 확인"""
    typer.echo("📊 시스템 상태 확인")
    
    config = load_config(config_file)
    
    # 설정 정보
    typer.echo(f"프로젝트: {config.project_id}")
    typer.echo(f"데이터셋: {config.dataset_id}")
    typer.echo(f"모드: {config.mode}")
    typer.echo(f"위치: {config.location}")
    
    # 아티팩트 확인
    artifacts_dir = Path("artifacts")
    if artifacts_dir.exists():
        files = list(artifacts_dir.glob("*"))
        typer.echo(f"아티팩트 파일 수: {len(files)}")
        
        for file in files:
            typer.echo(f"  - {file.name}")
    else:
        typer.echo("아티팩트 없음")
    
    # BigQuery 연결 확인
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=config.project_id)
        datasets = list(client.list_datasets())
        typer.echo(f"BigQuery 연결: ✅ ({len(datasets)}개 데이터셋)")
    except Exception as e:
        typer.echo(f"BigQuery 연결: ❌ ({e})")

if __name__ == "__main__":
    app()
