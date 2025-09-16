#!/usr/bin/env python3
"""
Multimodal Descent - 최종 검증 및 성능 지표 캡처
Kaggle BigQuery AI Hackathon 2024
"""

import os
import time
import json
from datetime import datetime
from google.cloud import bigquery
from src.descent import pipeline, config

def capture_performance_metrics():
    """성능 지표 캡처 및 저장"""
    print("📊 성능 지표 캡처 시작...")
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "project_id": config.GCP_PROJECT,
        "dataset_id": config.BQ_DATASET,
        "performance": {},
        "accuracy": {},
        "results": {}
    }
    
    # 파이프라인 실행 시간 측정
    start_time = time.time()
    
    try:
        # 1. 스키마 생성
        print("1. 스키마 생성...")
        schema_start = time.time()
        pipeline.step_schema()
        metrics["performance"]["schema_creation"] = time.time() - schema_start
        
        # 2. 샘플 데이터 삽입
        print("2. 샘플 데이터 삽입...")
        data_start = time.time()
        pipeline.step_sample_data()
        metrics["performance"]["data_insertion"] = time.time() - data_start
        
        # 3. 임베딩 생성
        print("3. 임베딩 생성...")
        embed_start = time.time()
        pipeline.step_embed()
        metrics["performance"]["embedding_generation"] = time.time() - embed_start
        
        # 4. ORI 최적화
        print("4. ORI 최적화...")
        ori_start = time.time()
        pipeline.step_ori_optimization()
        metrics["performance"]["ori_optimization"] = time.time() - ori_start
        
        # 5. 검색 테스트
        print("5. 검색 테스트...")
        search_start = time.time()
        pipeline.step_search("스펙과 이미지의 불일치 사례", 10)
        metrics["performance"]["vector_search"] = time.time() - search_start
        
        # 6. Before/After 비교
        print("6. Before/After 비교...")
        compare_start = time.time()
        pipeline.step_compare()
        metrics["performance"]["comparison"] = time.time() - compare_start
        
        total_time = time.time() - start_time
        metrics["performance"]["total_execution_time"] = total_time
        
        print(f"✅ 전체 파이프라인 실행 완료: {total_time:.2f}초")
        
    except Exception as e:
        print(f"❌ 파이프라인 실행 중 오류 발생: {e}")
        metrics["error"] = str(e)
        return metrics
    
    # 정확도 메트릭 계산
    print("📈 정확도 메트릭 계산...")
    try:
        client = bigquery.Client()
        
        # ORI 결과 조회
        ori_query = f"""
        SELECT 
          key,
          ori_score,
          risk_level,
          baseline_score,
          CASE 
            WHEN REGEXP_CONTAINS(body, r'(불일치|모순|다름)') THEN 1
            ELSE 0
          END AS actual_discrepancy
        FROM `{config.GCP_PROJECT}.{config.BQ_DATASET}.ori_results`
        ORDER BY ori_score DESC
        """
        
        ori_results = client.query(ori_query).to_dataframe()
        
        # 정확도 계산
        total_cases = len(ori_results)
        correct_predictions = len(ori_results[
            (ori_results['ori_score'] > 0.4) == (ori_results['actual_discrepancy'] == 1)
        ])
        
        # F1-Score 계산
        true_positives = len(ori_results[
            (ori_results['ori_score'] > 0.4) & (ori_results['actual_discrepancy'] == 1)
        ])
        false_positives = len(ori_results[
            (ori_results['ori_score'] > 0.4) & (ori_results['actual_discrepancy'] == 0)
        ])
        false_negatives = len(ori_results[
            (ori_results['ori_score'] <= 0.4) & (ori_results['actual_discrepancy'] == 1)
        ])
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # 베이스라인 정확도
        baseline_correct = len(ori_results[
            ori_results['baseline_score'] == ori_results['actual_discrepancy']
        ])
        baseline_accuracy = baseline_correct / total_cases if total_cases > 0 else 0
        
        metrics["accuracy"] = {
            "total_cases": total_cases,
            "correct_predictions": correct_predictions,
            "accuracy": correct_predictions / total_cases if total_cases > 0 else 0,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "baseline_accuracy": baseline_accuracy,
            "improvement_rate": ((correct_predictions / total_cases) - baseline_accuracy) / baseline_accuracy * 100 if baseline_accuracy > 0 else 0
        }
        
        # 결과 요약
        metrics["results"] = {
            "high_risk_cases": len(ori_results[ori_results['risk_level'] == 'HIGH']),
            "medium_risk_cases": len(ori_results[ori_results['risk_level'] == 'MEDIUM']),
            "low_risk_cases": len(ori_results[ori_results['risk_level'] == 'LOW']),
            "avg_ori_score": ori_results['ori_score'].mean(),
            "max_ori_score": ori_results['ori_score'].max(),
            "min_ori_score": ori_results['ori_score'].min()
        }
        
        print(f"✅ 정확도: {metrics['accuracy']['accuracy']:.2%}")
        print(f"✅ F1-Score: {metrics['accuracy']['f1_score']:.3f}")
        print(f"✅ 개선율: {metrics['accuracy']['improvement_rate']:.1f}%")
        
    except Exception as e:
        print(f"❌ 정확도 계산 중 오류 발생: {e}")
        metrics["accuracy_error"] = str(e)
    
    return metrics

def save_metrics(metrics):
    """메트릭을 JSON 파일로 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_metrics_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    print(f"📁 성능 지표 저장 완료: {filename}")
    return filename

def generate_report(metrics):
    """성능 보고서 생성"""
    print("\n" + "="*60)
    print("🎯 MULTIMODAL DESCENT 성능 보고서")
    print("="*60)
    
    print(f"\n📊 실행 시간 메트릭:")
    for key, value in metrics.get("performance", {}).items():
        print(f"  {key}: {value:.3f}초")
    
    print(f"\n🎯 정확도 메트릭:")
    accuracy = metrics.get("accuracy", {})
    print(f"  전체 사례: {accuracy.get('total_cases', 0)}")
    print(f"  정확한 예측: {accuracy.get('correct_predictions', 0)}")
    print(f"  정확도: {accuracy.get('accuracy', 0):.2%}")
    print(f"  정밀도: {accuracy.get('precision', 0):.3f}")
    print(f"  재현율: {accuracy.get('recall', 0):.3f}")
    print(f"  F1-Score: {accuracy.get('f1_score', 0):.3f}")
    print(f"  베이스라인 정확도: {accuracy.get('baseline_accuracy', 0):.2%}")
    print(f"  개선율: {accuracy.get('improvement_rate', 0):.1f}%")
    
    print(f"\n📈 결과 요약:")
    results = metrics.get("results", {})
    print(f"  HIGH 위험 사례: {results.get('high_risk_cases', 0)}")
    print(f"  MEDIUM 위험 사례: {results.get('medium_risk_cases', 0)}")
    print(f"  LOW 위험 사례: {results.get('low_risk_cases', 0)}")
    print(f"  평균 ORI 점수: {results.get('avg_ori_score', 0):.3f}")
    
    print("\n" + "="*60)

def main():
    """메인 실행 함수"""
    print("🚀 Multimodal Descent 최종 검증 시작")
    print("="*60)
    
    # 환경 변수 확인
    if not config.GCP_PROJECT or not config.BQ_DATASET:
        print("❌ 환경 변수가 설정되지 않았습니다.")
        print("   .env 파일을 생성하고 GCP_PROJECT, BQ_DATASET을 설정하세요.")
        return
    
    print(f"📋 프로젝트: {config.GCP_PROJECT}")
    print(f"📋 데이터셋: {config.BQ_DATASET}")
    
    # 성능 지표 캡처
    metrics = capture_performance_metrics()
    
    # 메트릭 저장
    filename = save_metrics(metrics)
    
    # 보고서 생성
    generate_report(metrics)
    
    print(f"\n🎉 검증 완료! 결과 파일: {filename}")
    print("="*60)

if __name__ == "__main__":
    main()
