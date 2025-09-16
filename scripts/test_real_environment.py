#!/usr/bin/env python3
"""
Multimodal Descent - 실제 환경 테스트 스크립트
간단한 설정으로 바로 실행 가능
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """필수 요구사항 확인"""
    print("🔍 필수 요구사항 확인 중...")
    
    # Python 버전 확인
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        return False
    
    # 필요한 패키지 확인
    required_packages = [
        'google-cloud-bigquery',
        'pandas',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 다음 패키지들이 설치되지 않았습니다: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ 모든 필수 요구사항이 충족되었습니다.")
    return True

def setup_environment():
    """환경 설정"""
    print("\n⚙️ 환경 설정 중...")
    
    # .env 파일 확인
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 .env 파일을 생성합니다...")
        
        # 사용자로부터 프로젝트 ID 입력 받기
        project_id = input("GCP 프로젝트 ID를 입력하세요: ").strip()
        if not project_id:
            print("❌ 프로젝트 ID가 필요합니다.")
            return False
        
        # .env 파일 생성
        env_content = f"""# Multimodal Descent 환경 설정
GCP_PROJECT={project_id}
BQ_DATASET=descent_demo
BQ_LOCATION=US
USE_REAL_EMBEDDINGS=false
EMBEDDING_MODEL=textembedding-gecko@001
ORI_WEIGHT=0.7
ORI_THRESHOLD=0.3
TOP_K_RESULTS=10
BATCH_SIZE=1000
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print(f"✅ .env 파일이 생성되었습니다. (프로젝트: {project_id})")
    else:
        print("✅ .env 파일이 이미 존재합니다.")
    
    return True

def test_gcp_connection():
    """GCP 연결 테스트"""
    print("\n🔗 GCP 연결 테스트 중...")
    
    try:
        from google.cloud import bigquery
        from dotenv import load_dotenv
        
        load_dotenv()
        
        project_id = os.getenv("GCP_PROJECT")
        if not project_id:
            print("❌ GCP_PROJECT가 .env 파일에 설정되지 않았습니다.")
            return False
        
        # BigQuery 클라이언트 생성 및 테스트
        client = bigquery.Client(project=project_id)
        
        # 간단한 쿼리로 연결 테스트
        query = "SELECT 1 as test"
        result = client.query(query).result()
        
        print(f"✅ GCP 연결 성공! (프로젝트: {project_id})")
        return True
        
    except Exception as e:
        print(f"❌ GCP 연결 실패: {e}")
        print("\n해결 방법:")
        print("1. gcloud auth login")
        print("2. gcloud auth application-default login")
        print("3. gcloud config set project YOUR_PROJECT_ID")
        return False

def run_pipeline():
    """파이프라인 실행"""
    print("\n🚀 파이프라인 실행 중...")
    
    try:
        # Python 모듈로 파이프라인 실행
        commands = [
            ["python", "-m", "src.descent.pipeline", "schema"],
            ["python", "-m", "src.descent.pipeline", "sample_data"],
            ["python", "-m", "src.descent.pipeline", "embed"],
            ["python", "-m", "src.descent.pipeline", "ori"],
            ["python", "-m", "src.descent.pipeline", "search"],
            ["python", "-m", "src.descent.pipeline", "compare"]
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}/6: {' '.join(cmd[2:])}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ 명령어 실행 실패: {' '.join(cmd)}")
                print(f"오류: {result.stderr}")
                return False
            else:
                print(f"  ✅ 완료")
        
        print("✅ 전체 파이프라인 실행 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 파이프라인 실행 중 오류: {e}")
        return False

def show_results():
    """결과 표시"""
    print("\n📊 결과 확인 중...")
    
    try:
        from google.cloud import bigquery
        from dotenv import load_dotenv
        
        load_dotenv()
        
        project_id = os.getenv("GCP_PROJECT")
        dataset_id = os.getenv("BQ_DATASET", "descent_demo")
        
        client = bigquery.Client(project=project_id)
        
        # ORI 결과 조회
        query = f"""
        SELECT 
          key,
          ori_score,
          risk_level,
          body
        FROM `{project_id}.{dataset_id}.ori_results`
        ORDER BY ori_score DESC
        """
        
        results = client.query(query).to_dataframe()
        
        print("\n🎯 ORI 분석 결과:")
        print("=" * 80)
        for _, row in results.iterrows():
            print(f"ID: {row['key']}")
            print(f"ORI 점수: {row['ori_score']:.3f}")
            print(f"위험도: {row['risk_level']}")
            print(f"내용: {row['body'][:50]}...")
            print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ 결과 조회 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 Multimodal Descent 실제 환경 테스트")
    print("=" * 50)
    
    # 1. 요구사항 확인
    if not check_requirements():
        return
    
    # 2. 환경 설정
    if not setup_environment():
        return
    
    # 3. GCP 연결 테스트
    if not test_gcp_connection():
        return
    
    # 4. 파이프라인 실행
    if not run_pipeline():
        return
    
    # 5. 결과 표시
    show_results()
    
    print("\n🎉 테스트 완료!")
    print("=" * 50)
    print("다음 단계:")
    print("1. python validate_pipeline.py - 성능 검증")
    print("2. BigQuery Console에서 결과 확인")
    print("3. 실제 데이터로 테스트")

if __name__ == "__main__":
    main()
