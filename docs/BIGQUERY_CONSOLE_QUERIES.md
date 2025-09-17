# BigQuery Console 실행 쿼리 모음
# BigQuery AI Hackathon 2024 - 데모 영상용

## 🎯 쿼리 실행 순서 및 목적

### 1️⃣ 텍스트 임베딩 차원 확인 (768차원)
**목적**: Vertex AI 텍스트 임베딩의 차원 수 확인
**예상 결과**: embedding_dim = 768

```sql
-- 텍스트 임베딩 차원 확인
SELECT 
  id,
  ARRAY_LENGTH(embedding) as embedding_dim,
  text_content
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 5;
```

### 2️⃣ 이미지 임베딩 차원 확인 (1408차원)
**목적**: Vertex AI 이미지 임베딩의 차원 수 확인
**예상 결과**: embedding_dim = 1408

```sql
-- 이미지 임베딩 차원 확인
SELECT 
  id,
  uri,
  ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real` 
LIMIT 5;
```

### 3️⃣ 멀티모달 통합 차원 확인 (2179차원)
**목적**: 텍스트 + 이미지 + 구조화 데이터 통합 임베딩의 차원 수 확인
**예상 결과**: total_dimensions = 2179 (768 + 1408 + 3)

```sql
-- 멀티모달 통합 임베딩 차원 확인
SELECT 
  key,
  ARRAY_LENGTH(embedding) as total_dimensions,
  text_id,
  image_id
FROM `${GCP_PROJECT_ID}.descent_demo.emb_stitched_mm` 
LIMIT 5;
```

### 4️⃣ 멀티모달 차원 비교 테이블
**목적**: 각 모달리티별 임베딩 차원을 한눈에 비교
**예상 결과**: text=768, image=1408, struct=3, total=2179

```sql
-- 멀티모달 차원 비교
SELECT 'text' as type, ARRAY_LENGTH(embedding) as dimensions 
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 1 
UNION ALL 
SELECT 'image' as type, ARRAY_LENGTH(embedding) as dimensions 
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real` 
LIMIT 1 
UNION ALL 
SELECT 'struct' as type, ARRAY_LENGTH(embedding) as dimensions 
FROM `${GCP_PROJECT_ID}.descent_demo.feat_struct_vec` 
LIMIT 1;
```

### 5️⃣ ORI 분석 결과 확인
**목적**: ORI 알고리즘의 실행 결과 확인
**예상 결과**: HIGH/MEDIUM/LOW 위험도 분포

```sql
-- ORI 분석 결과 확인
SELECT 
  risk_level,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM `${GCP_PROJECT_ID}.descent_demo.ori_results` 
GROUP BY risk_level
ORDER BY 
  CASE risk_level 
    WHEN 'HIGH' THEN 1 
    WHEN 'MEDIUM' THEN 2 
    WHEN 'LOW' THEN 3 
  END;
```

### 6️⃣ 성능 지표 비교 테이블
**목적**: Baseline vs Descent 성능 비교
**예상 결과**: F1-Score +300%, Processing Time -85% 등

```sql
-- 성능 지표 비교
SELECT 
  metric,
  baseline_value,
  descent_value,
  ROUND((descent_value - baseline_value) / baseline_value * 100, 0) as improvement_percent
FROM `${GCP_PROJECT_ID}.descent_demo.performance_metrics`
ORDER BY improvement_percent DESC;
```

## 🎬 데모 영상 촬영 가이드

### 촬영 순서:
1. **CLI 실행** (터미널 화면)
2. **BigQuery Console 접속** (브라우저)
3. **쿼리 1-6 순차 실행** (BigQuery Console)
4. **결과 확인 및 설명** (화면 공유)
5. **최종 아티팩트 확인** (파일 탐색기)

### 촬영 팁:
- 각 쿼리 실행 후 결과가 완전히 로드될 때까지 대기
- 중요한 숫자들 (768, 1408, 2179)을 강조
- 성능 개선 수치 (+300%, -85%)를 명확히 표시
- 전체 화면 모드로 촬영하여 가독성 확보

### 예상 촬영 시간:
- CLI 실행: 30초
- BigQuery 쿼리 실행: 3분
- 결과 설명: 2분
- 총 예상 시간: 5-6분

## 📋 체크리스트

- [ ] BigQuery Console 접속 확인
- [ ] 프로젝트 ID 설정 확인 (${GCP_PROJECT_ID})
- [ ] 데이터셋 존재 확인 (descent_demo)
- [ ] 각 쿼리 실행 및 결과 확인
- [ ] 스크린샷 캡처 (필요시)
- [ ] 영상 촬영 완료
- [ ] 영상 편집 및 업로드 준비
