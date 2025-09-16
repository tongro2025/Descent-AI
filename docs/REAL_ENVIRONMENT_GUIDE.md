# 실제 환경 실행 가이드

## 🚀 Step 1: GCP 프로젝트 설정

### 1.1 GCP 프로젝트 생성
```bash
# Google Cloud Console에서 새 프로젝트 생성
# 또는 기존 프로젝트 사용
# 프로젝트 ID를 기록해두세요 (예: my-descent-project-123)
```

### 1.2 BigQuery API 활성화
```bash
# Google Cloud Console에서:
# 1. APIs & Services > Library 이동
# 2. "BigQuery API" 검색
# 3. "Enable" 클릭

# 또는 gcloud CLI 사용:
gcloud services enable bigquery.googleapis.com
```

### 1.3 인증 설정
```bash
# gcloud CLI 설치 (이미 설치되어 있다면 건너뛰기)
# https://cloud.google.com/sdk/docs/install

# 인증
gcloud auth login
gcloud auth application-default login

# 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID
```

## 🔧 Step 2: 로컬 환경 설정

### 2.1 저장소 클론 및 이동
```bash
# 현재 디렉토리에서 실행
cd /Users/hakjun/Desktop/Descent

# 또는 GitHub에서 클론하는 경우:
# git clone https://github.com/your-username/multimodal-descent.git
# cd multimodal-descent
```

### 2.2 가상환경 생성 및 활성화
```bash
# Python 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
# venv\Scripts\activate
```

### 2.3 의존성 설치
```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 추가로 필요한 패키지들
pip install google-cloud-bigquery
pip install pandas
pip install matplotlib
pip install seaborn
```

## ⚙️ Step 3: 환경 변수 설정

### 3.1 .env 파일 생성
```bash
# env.example을 복사하여 .env 생성
cp env.example .env

# .env 파일 편집
nano .env  # 또는 vim .env, code .env
```

### 3.2 .env 파일 내용 설정
```bash
# .env 파일 내용
GCP_PROJECT=your-actual-project-id
BQ_DATASET=descent_demo
BQ_LOCATION=US
GCS_BUCKET=gs://your-bucket-name
USE_REAL_EMBEDDINGS=false
EMBEDDING_MODEL=textembedding-gecko@001
ORI_WEIGHT=0.7
ORI_THRESHOLD=0.3
TOP_K_RESULTS=10
BATCH_SIZE=1000
```

**중요**: `your-actual-project-id`를 실제 GCP 프로젝트 ID로 변경하세요!

## 🏃‍♂️ Step 4: 파이프라인 실행

### 4.1 전체 파이프라인 실행
```bash
# Makefile 사용 (권장)
make init && make sample_data && make embed && make ori && make search && make compare

# 또는 개별 실행
python -m src.descent.pipeline schema
python -m src.descent.pipeline sample_data
python -m src.descent.pipeline embed
python -m src.descent.pipeline ori
python -m src.descent.pipeline search
python -m src.descent.pipeline compare
```

### 4.2 성능 검증
```bash
# 성능 지표 캡처 및 검증
python validate_pipeline.py
```

## 🔍 Step 5: 결과 확인

### 5.1 BigQuery Console에서 확인
```sql
-- BigQuery Console에서 실행
SELECT * FROM `your-project-id.descent_demo.ori_results`
ORDER BY ori_score DESC;
```

### 5.2 Python에서 결과 조회
```python
from google.cloud import bigquery

client = bigquery.Client()
query = """
SELECT * FROM `your-project-id.descent_demo.ori_results`
ORDER BY ori_score DESC
"""
results = client.query(query).to_dataframe()
print(results)
```

## 🐛 문제 해결

### 일반적인 오류들

#### 1. 인증 오류
```bash
# 해결 방법
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

#### 2. BigQuery API 비활성화
```bash
# 해결 방법
gcloud services enable bigquery.googleapis.com
```

#### 3. 권한 부족
```bash
# BigQuery Admin 권한 필요
# Google Cloud Console > IAM & Admin > IAM에서 확인
```

#### 4. 프로젝트 ID 오류
```bash
# .env 파일의 GCP_PROJECT 확인
# gcloud config get-value project 로 현재 프로젝트 확인
```

## 📊 성공적인 실행 확인

### 실행 성공 시 나타나는 메시지들
```
[OK] schema ready
[OK] Ran: sql/05_sample_data.sql
[OK] Ran: sql/02_embeddings.sql
[OK] Ran: sql/12_ori_optimization.sql
[OK] Ran: sql/04_search_demo.sql
[OK] Ran: sql/06_before_after.sql
```

### 성능 지표 예시
```
📊 성능 지표:
  전체 사례: 6
  정확한 예측: 6
  정확도: 100.00%
  F1-Score: 0.920
  개선율: 300.0%
```

## 🎯 다음 단계

1. **실제 데이터 적용**: 샘플 데이터 대신 실제 제품 데이터 사용
2. **실제 임베딩 모델**: textembedding-gecko@001 사용
3. **대규모 데이터**: 수백만 건 데이터 처리
4. **실시간 모니터링**: 스트리밍 데이터 처리

---

**💡 팁**: 처음 실행할 때는 더미 임베딩을 사용하여 빠르게 테스트하고, 정상 작동 확인 후 실제 임베딩 모델로 전환하세요!
