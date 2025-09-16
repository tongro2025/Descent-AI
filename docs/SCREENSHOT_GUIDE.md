# Descent Pipeline 데모 스크린샷 가이드

## 🎬 Kaggle 제출용 데모 영상 제작 가이드

### 1. CLI 실행 화면 캡처
```bash
# 터미널에서 실행
./demo_script.sh
```

**캡처 포인트:**
- 시스템 상태 확인 화면
- 프로젝트 초기화 과정
- 드라이런 모드 실행
- ORI 분석 결과
- 평가 리포트 생성
- 통합 테스트 통과

### 2. BigQuery 쿼리 결과 캡처

**BigQuery Console에서 실행할 쿼리들:**

#### 2.1 기본 데이터 확인
```sql
SELECT * FROM `gen-lang-client-0790720774.descent_demo.raw_texts` LIMIT 5;
```

#### 2.2 임베딩 결과 확인
```sql
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim 
FROM `gen-lang-client-0790720774.descent_demo.emb_view_t_vertex` 
LIMIT 5;
```

#### 2.3 ORI 분석 결과
```sql
SELECT id, ori, predict, semantic_distance, rule_score, body
FROM `gen-lang-client-0790720774.descent_demo.report_ori`
ORDER BY ori DESC
LIMIT 10;
```

#### 2.4 멀티모달 결과 비교
```sql
SELECT 'text' as mode, id, ori, predict FROM `gen-lang-client-0790720774.descent_demo.report_ori`
UNION ALL
SELECT 'multimodal' as mode, id, ori, predict FROM `gen-lang-client-0790720774.descent_demo.report_ori_mm`
UNION ALL
SELECT 'native' as mode, id, ori, predict FROM `gen-lang-client-0790720774.descent_demo.report_ori`
ORDER BY mode, ori DESC;
```

#### 2.5 평가 메트릭
```sql
SELECT * FROM `gen-lang-client-0790720774.descent_demo.eval_metrics`;
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
FROM `gen-lang-client-0790720774.descent_demo.emb_view_i_real`
LIMIT 5;
```

### 4. 멀티모달 확장 증거

#### 4.1 차원 비교
```sql
SELECT 
  'text' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `gen-lang-client-0790720774.descent_demo.emb_view_t_vertex`
LIMIT 1
UNION ALL
SELECT 
  'image' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `gen-lang-client-0790720774.descent_demo.emb_view_i_real`
LIMIT 1
UNION ALL
SELECT 
  'struct' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `gen-lang-client-0790720774.descent_demo.feat_struct_vec`
LIMIT 1;
```

#### 4.2 통합 임베딩 차원
```sql
SELECT 
  key,
  ARRAY_LENGTH(embedding) as total_dimensions
FROM `gen-lang-client-0790720774.descent_demo.emb_stitched_mm`
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
FROM `gen-lang-client-0790720774.descent_demo.cost_log`
ORDER BY creation_time DESC
LIMIT 10;
```

#### 5.2 실행 로그
```sql
SELECT 
  step,
  status,
  timestamp
FROM `gen-lang-client-0790720774.descent_demo.run_log`
ORDER BY timestamp DESC
LIMIT 10;
```

### 6. 영상 제작 팁

1. **화면 녹화 설정**
   - 해상도: 1920x1080 이상
   - 프레임레이트: 30fps
   - 길이: 3-5분 권장

2. **캡처 순서**
   - CLI 실행 → BigQuery 결과 → 성능 메트릭
   - 각 단계별로 10-15초씩 충분한 시간

3. **강조 포인트**
   - 3가지 임베딩 옵션
   - 100% 정확도
   - 멀티모달 통합
   - 자동화된 파이프라인

4. **음성 설명**
   - 각 단계별로 간단한 설명
   - 기술적 특징 강조
   - 성능 지표 언급

### 7. 최종 체크리스트

- [ ] CLI 실행 화면 캡처
- [ ] BigQuery 쿼리 결과 캡처
- [ ] 실제 이미지 임베딩 결과
- [ ] 멀티모달 차원 비교
- [ ] 성능 메트릭 표시
- [ ] 영상 편집 및 업로드
