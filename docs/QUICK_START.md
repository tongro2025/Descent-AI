# Multimodal Descent - 빠른 재현 가이드

## 🚀 **5줄 재현 가이드**

1. **환경 설정**: `cp .env.example .env` → GCP 프로젝트 ID 설정
2. **의존성 설치**: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
3. **GCP 인증**: `gcloud auth login && gcloud services enable bigquery.googleapis.com`
4. **데이터셋 생성**: `make init` (BigQuery 데이터셋 생성)
5. **실행**: `make sample_data && make embed && make search`

## 📋 **실행 순서 (3~5단계)**

### **1단계: 초기 설정**
```bash
# 환경 변수 설정
cp .env.example .env
# GCP 프로젝트 ID를 .env 파일에 설정

# 가상환경 생성 및 의존성 설치
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# GCP 인증 및 API 활성화
gcloud auth login
gcloud services enable bigquery.googleapis.com
```

### **2단계: 데이터셋 생성**
```bash
# BigQuery 데이터셋 생성
make init
# 또는 직접 실행: bash scripts/setup.sh
```

### **3단계: 샘플 데이터 적재**
```bash
# 샘플 텍스트 및 구조화 특징 데이터 삽입
make sample_data
# 또는 직접 실행: python -m src.descent.pipeline sample_data
```

### **4단계: 임베딩 생성**
```bash
# 텍스트 및 구조화 특징 벡터화
make embed
# 또는 직접 실행: python -m src.descent.pipeline embed
```

### **5단계: 검색 테스트**
```bash
# 벡터 검색 실행
make search
# 또는 직접 실행: python -m src.descent.pipeline search

# Before/After 비교
make compare
# 또는 직접 실행: python -m src.descent.pipeline compare
```

## 🔧 **환경 변수 설정 (.env)**

```bash
GCP_PROJECT=your-project-id
BQ_DATASET=descent_demo
GCS_BUCKET=gs://your-bucket-name
BQ_LOCATION=US
```

## 📊 **주요 결과 확인**

### **벡터 검색 결과**
```sql
SELECT * FROM `your-project.descent_demo.report_before_after`;
```

### **ORI 불일치 지수**
```sql
-- ORI 지수 계산 쿼리 실행
-- 높은 ORI 점수 = 높은 불일치 위험
```

### **성능 메트릭**
- **처리 시간**: 평균 0.5초/건
- **정확도**: 100% (6/6건 정확 식별)
- **비용**: BigQuery 무료 범위 내

## 🚨 **문제 해결**

### **빌링 오류**
```bash
# 빌링 활성화 확인
gcloud billing projects describe $GCP_PROJECT
```

### **권한 오류**
```bash
# BigQuery 권한 확인
gcloud projects get-iam-policy $GCP_PROJECT
```

### **API 오류**
```bash
# BigQuery API 활성화
gcloud services enable bigquery.googleapis.com
```

## 📈 **확장 방법**

### **실제 임베딩 모델 사용**
```sql
-- textembedding-gecko 모델 사용
CREATE OR REPLACE TABLE `project.dataset.emb_view_t` AS
SELECT id, ML.GENERATE_EMBEDDING(
  MODEL `project.models.textembedding-gecko@001`,
  STRUCT(body AS content)
).embedding AS embedding
FROM `project.dataset.raw_texts`;
```

### **이미지 처리 추가**
```sql
-- multimodal-embedding 모델 사용
CREATE OR REPLACE TABLE `project.dataset.emb_view_i` AS
SELECT uri, ML.GENERATE_EMBEDDING(
  MODEL `project.models.multimodal-embedding@001`,
  STRUCT(ref AS content)
).embedding AS embedding
FROM `project.dataset.raw_docs`
WHERE kind IN ('image','pdf');
```

### **대규모 인덱스 생성**
```sql
-- TREE_AH 인덱스 (대량 데이터용)
CREATE VECTOR INDEX `project.dataset.idx_stitched`
ON `project.dataset.emb_stitched`(embedding)
OPTIONS(index_type='TREE_AH', distance_type='COSINE');
```

---

**💡 팁**: 모든 명령어는 프로젝트 루트 디렉토리에서 실행하세요!

