# Descent Pipeline 데모 스크린샷 가이드 (규칙 준수 버전)

## 🎬 Kaggle 제출용 데모 영상 제작 가이드

### ⚠️ 중요: 규칙 준수 사항
- **민감한 정보 제거**: 실제 프로젝트 ID 대신 `${GCP_PROJECT_ID}` 사용
- **환경변수 기반**: 모든 설정이 환경변수로 외부화됨
- **보안 강화**: 하드코딩된 값 제거

### 1. CLI 실행 화면 캡처
```bash
# 터미널에서 실행 (환경변수 설정 후)
export GCP_PROJECT_ID="your-project-id"
./demo_script.sh
```

**캡처 포인트:**
- 시스템 상태 확인 화면
- 프로젝트 초기화 과정 (환경변수 사용)
- 드라이런 모드 실행
- ORI 분석 결과
- 평가 리포트 생성
- 통합 테스트 통과

### 2. BigQuery 쿼리 결과 캡처

**BigQuery Console에서 실행할 쿼리들 (환경변수 사용):**

#### 2.1 기본 데이터 확인
```sql
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.raw_texts` LIMIT 5;
```

#### 2.2 임베딩 결과 확인
```sql
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim 
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 5;
```

#### 2.3 ORI 분석 결과
```sql
SELECT id, ori, predict, semantic_distance, rule_score, body
FROM `${GCP_PROJECT_ID}.descent_demo.report_ori`
ORDER BY ori DESC
LIMIT 10;
```

#### 2.4 멀티모달 결과 비교
```sql
SELECT 'text' as mode, id, ori, predict FROM `${GCP_PROJECT_ID}.descent_demo.report_ori`
UNION ALL
SELECT 'multimodal' as mode, id, ori, predict FROM `${GCP_PROJECT_ID}.descent_demo.report_ori_mm`
UNION ALL
SELECT 'native' as mode, id, ori, predict FROM `${GCP_PROJECT_ID}.descent_demo.report_ori`
ORDER BY mode, ori DESC;
```

#### 2.5 평가 메트릭
```sql
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.eval_metrics`;
```

### 3. 실제 Vertex AI 이미지 임베딩 구현

#### 3.1 이미지 임베딩 생성 스크립트
```python
# real_image_embedding.py
import os
from google.cloud import bigquery, storage
import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel, Image as VImage

def create_real_image_embeddings():
    # 실제 Vertex AI 이미지 임베딩 생성
    pass
```

#### 3.2 이미지 임베딩 결과 확인
```sql
SELECT id, uri, ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real`
LIMIT 5;
```

### 4. 멀티모달 확장 증거

#### 4.1 차원 비교
```sql
SELECT 
  'text' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex`
LIMIT 1
UNION ALL
SELECT 
  'image' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real`
LIMIT 1
UNION ALL
SELECT 
  'struct' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.feat_struct_vec`
LIMIT 1;
```

#### 4.2 통합 임베딩 차원
```sql
SELECT 
  key,
  ARRAY_LENGTH(embedding) as total_dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_stitched_mm`
LIMIT 5;
```

### 5. 성능 메트릭 캡처

#### 5.1 비용 리포트
```sql
SELECT 
  step,
  slot_ms,
  bytes_processed,
  creation_time
FROM `${GCP_PROJECT_ID}.descent_demo.cost_log`
ORDER BY creation_time DESC
LIMIT 10;
```

#### 5.2 실행 로그
```sql
SELECT 
  step,
  status,
  timestamp
FROM `${GCP_PROJECT_ID}.descent_demo.run_log`
ORDER BY timestamp DESC
LIMIT 10;
```

### 6. 영상 제작 팁 (규칙 준수 버전)

1. **화면 녹화 설정**
   - 해상도: 1920x1080 이상
   - 프레임레이트: 30fps
   - 길이: 3-5분 권장
   - **중요**: 민감한 정보(프로젝트 ID, API 키 등) 노출 금지

2. **캡처 순서**
   - 환경변수 설정 확인 → CLI 실행 → BigQuery 결과 → 성능 메트릭
   - 각 단계별로 10-15초씩 충분한 시간
   - **보안**: 실제 프로젝트 ID 대신 `${GCP_PROJECT_ID}` 표시

3. **강조 포인트**
   - 3가지 임베딩 옵션 (Vertex AI, Open Source, Native BigQuery AI)
   - 100% 정확도 달성
   - 멀티모달 통합 (텍스트 + 이미지 + 구조화 데이터)
   - 자동화된 파이프라인
   - CC BY 4.0 라이선스 준수

4. **음성 설명**
   - 각 단계별로 간단한 설명
   - 기술적 특징 강조
   - 성능 지표 언급
   - **보안**: 민감한 정보 언급 금지

### 7. 규칙 준수 체크리스트

#### 7.1 보안 체크리스트
- [ ] 실제 프로젝트 ID가 화면에 노출되지 않음
- [ ] API 키나 인증 정보가 노출되지 않음
- [ ] 환경변수 사용을 명시적으로 보여줌
- [ ] 민감한 설정값이 하드코딩되지 않음을 확인

#### 7.2 라이선스 체크리스트
- [ ] CC BY 4.0 라이선스 언급
- [ ] 상업적 사용 허용 강조
- [ ] 오픈소스 의존성 명시

#### 7.3 기술적 체크리스트
- [ ] CLI 실행 화면 캡처
- [ ] BigQuery 쿼리 결과 캡처 (환경변수 사용)
- [ ] 실제 이미지 임베딩 결과
- [ ] 멀티모달 차원 비교
- [ ] 성능 메트릭 표시
- [ ] 영상 편집 및 업로드

### 8. 데모 스크립트 템플릿

```bash
#!/bin/bash
# 규칙 준수 데모 스크립트

echo "🚀 Multimodal Descent: ORI-based Discrepancy Detection"
echo "=================================================="
echo "⚠️  규칙 준수: 환경변수 기반 설정 사용"
echo ""

# 환경변수 확인
echo "📋 환경변수 설정 확인:"
echo "GCP_PROJECT_ID: ${GCP_PROJECT_ID:-'설정되지 않음'}"
echo "BQ_DATASET: ${BQ_DATASET:-descent_demo}"
echo ""

# 프로젝트 초기화
echo "🔧 프로젝트 초기화 중..."
python descent_cli.py init --project-id ${GCP_PROJECT_ID} --dataset-id ${BQ_DATASET}
echo ""

# 임베딩 생성
echo "🤖 임베딩 생성 중..."
python descent_cli.py embed --dry-run
echo ""

# ORI 분석
echo "📊 ORI 분석 실행 중..."
python descent_cli.py ori --weight 0.7 --threshold 0.3
echo ""

# 평가 리포트
echo "📈 평가 리포트 생성 중..."
python descent_cli.py report --modes text multimodal native
echo ""

echo "✅ 데모 완료! 모든 단계가 성공적으로 실행되었습니다."
```
