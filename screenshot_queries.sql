-- BigQuery 스크린샷용 쿼리 모음 (규칙 준수 버전)
-- 모든 쿼리는 환경변수 ${GCP_PROJECT_ID} 사용

-- 1. 기본 데이터 확인
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.raw_texts` LIMIT 5;

-- 2. 텍스트 임베딩 결과 확인
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim 
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 5;

-- 3. 이미지 임베딩 결과 확인
SELECT id, uri, ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real`
LIMIT 5;

-- 4. 구조화 데이터 임베딩 확인
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.feat_struct_vec`
LIMIT 5;

-- 5. ORI 분석 결과
SELECT id, ori, predict, semantic_distance, rule_score, body
FROM `${GCP_PROJECT_ID}.descent_demo.report_ori`
ORDER BY ori DESC
LIMIT 10;

-- 6. 멀티모달 차원 비교
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

-- 7. 통합 임베딩 결과
SELECT 
  key,
  ARRAY_LENGTH(embedding) as total_dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_stitched_mm`
LIMIT 5;

-- 8. 성능 메트릭
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.eval_metrics`;

-- 9. 비용 리포트
SELECT 
  step,
  slot_ms,
  bytes_processed,
  creation_time
FROM `${GCP_PROJECT_ID}.descent_demo.cost_log`
ORDER BY creation_time DESC
LIMIT 10;

-- 10. 실행 로그
SELECT 
  step,
  status,
  timestamp
FROM `${GCP_PROJECT_ID}.descent_demo.run_log`
ORDER BY timestamp DESC
LIMIT 10;
