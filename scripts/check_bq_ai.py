#!/usr/bin/env python3
"""
BigQuery AI 모델 가용성 확인 스크립트
옵션 A 구현 전 필수 확인사항
"""

import os
from google.cloud import bigquery
from dotenv import load_dotenv

def check_bigquery_ai_availability():
    """BigQuery AI 모델 가용성 확인"""
    print("🔍 BigQuery AI 모델 가용성 확인 중...")
    
    load_dotenv()
    project_id = os.getenv("GCP_PROJECT")
    
    if not project_id:
        print("❌ GCP_PROJECT가 .env 파일에 설정되지 않았습니다.")
        return False
    
    try:
        client = bigquery.Client(project=project_id)
        
        # 1. 프로젝트 정보 확인
        print(f"📋 프로젝트: {project_id}")
        
        # 2. BigQuery AI 모델 목록 확인
        print("\n🤖 사용 가능한 BigQuery AI 모델 확인...")
        
        # 텍스트 임베딩 모델 확인
        text_models_query = """
        SELECT model_name, model_type, creation_time
        FROM `INFORMATION_SCHEMA.MODELS`
        WHERE model_type = 'TEXT_EMBEDDING'
        ORDER BY creation_time DESC
        """
        
        try:
            text_models = client.query(text_models_query).result()
            print("✅ 텍스트 임베딩 모델:")
            for model in text_models:
                print(f"  - {model.model_name} ({model.model_type})")
        except Exception as e:
            print(f"⚠️ 텍스트 임베딩 모델 확인 실패: {e}")
            print("  기본 모델 사용을 시도합니다.")
        
        # 3. 기본 모델 테스트
        print("\n🧪 기본 텍스트 임베딩 모델 테스트...")
        
        test_query = """
        SELECT 
          ML.GENERATE_EMBEDDING(
            MODEL `models.text_embedding`,
            STRUCT('테스트 텍스트' AS content)
          ).embedding AS embedding
        """
        
        try:
            result = client.query(test_query).result()
            for row in result:
                embedding = row.embedding
                print(f"✅ 기본 모델 테스트 성공!")
                print(f"  임베딩 차원: {len(embedding)}")
                print(f"  첫 5개 값: {embedding[:5]}")
                return True
        except Exception as e:
            print(f"❌ 기본 모델 테스트 실패: {e}")
            print("\n해결 방법:")
            print("1. BigQuery Studio에서 AI functions 탭 확인")
            print("2. 프로젝트/리전이 모델 가용 리전과 일치하는지 확인")
            print("3. BigQuery JobUser + Vertex AI 사용 권한 확인")
            return False
            
    except Exception as e:
        print(f"❌ BigQuery 연결 실패: {e}")
        return False

def check_multimodal_availability():
    """멀티모달 임베딩 모델 가용성 확인"""
    print("\n🖼️ 멀티모달 임베딩 모델 확인...")
    
    load_dotenv()
    project_id = os.getenv("GCP_PROJECT")
    
    try:
        client = bigquery.Client(project=project_id)
        
        # 멀티모달 모델 확인
        multimodal_query = """
        SELECT model_name, model_type, creation_time
        FROM `INFORMATION_SCHEMA.MODELS`
        WHERE model_type = 'MULTIMODAL_EMBEDDING'
        ORDER BY creation_time DESC
        """
        
        try:
            multimodal_models = client.query(multimodal_query).result()
            print("✅ 멀티모달 임베딩 모델:")
            for model in multimodal_models:
                print(f"  - {model.model_name} ({model.model_type})")
            return True
        except Exception as e:
            print(f"⚠️ 멀티모달 모델 확인 실패: {e}")
            print("  텍스트만 사용합니다.")
            return False
            
    except Exception as e:
        print(f"❌ 멀티모달 모델 확인 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 BigQuery AI 모델 가용성 확인")
    print("=" * 50)
    
    # 텍스트 임베딩 모델 확인
    text_available = check_bigquery_ai_availability()
    
    # 멀티모달 모델 확인
    multimodal_available = check_multimodal_availability()
    
    print("\n📊 확인 결과:")
    print(f"  텍스트 임베딩: {'✅ 사용 가능' if text_available else '❌ 사용 불가'}")
    print(f"  멀티모달 임베딩: {'✅ 사용 가능' if multimodal_available else '❌ 사용 불가'}")
    
    if text_available:
        print("\n🎉 옵션 A (BigQuery AI SQL) 사용 가능!")
        print("다음 단계: 실제 임베딩 모델로 파이프라인 실행")
    else:
        print("\n⚠️ 옵션 A 사용 불가 - 옵션 B 또는 C 사용 권장")
        print("옵션 B: Vertex AI Python SDK")
        print("옵션 C: 오픈소스 임베딩 모델")

if __name__ == "__main__":
    main()
