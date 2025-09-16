-- 증분 임베딩 및 아이도포턴시 구현
-- P1: 성능·스케일 개선

-- 1. 콘텐츠 해시 추가 (아이도포턴시)
ALTER TABLE `${PROJECT}.${DATASET}.raw_texts`
ADD COLUMN IF NOT EXISTS content_hash INT64;

UPDATE `${PROJECT}.${DATASET}.raw_texts`
SET content_hash = FARM_FINGERPRINT(CONCAT(body))
WHERE content_hash IS NULL;

-- 2. 임베딩 작업 상태 테이블 생성
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.emb_jobs_status` (
  id STRING,
  content_hash INT64,
  embedding_type STRING, -- 'text', 'image', 'struct'
  status STRING, -- 'pending', 'processing', 'completed', 'failed'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  error_message STRING
);

-- 3. 증분 텍스트 임베딩 (새로 들어온 행만)
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.emb_text_new` AS
SELECT t.id, t.body, t.content_hash
FROM `${PROJECT}.${DATASET}.raw_texts` t
LEFT JOIN `${PROJECT}.${DATASET}.emb_jobs_status` s 
  ON t.id = s.id AND s.embedding_type = 'text' AND s.status = 'completed'
WHERE s.id IS NULL;

-- 4. 증분 구조화 특징 임베딩
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.emb_struct_new` AS
SELECT f.id, f.f1, f.f2, f.f3, t.content_hash
FROM `${PROJECT}.${DATASET}.feat_struct` f
LEFT JOIN `${PROJECT}.${DATASET}.raw_texts` t ON f.id = t.id
LEFT JOIN `${PROJECT}.${DATASET}.emb_jobs_status` s 
  ON f.id = s.id AND s.embedding_type = 'struct' AND s.status = 'completed'
WHERE s.id IS NULL;

-- 5. 증분 이미지 임베딩
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.emb_image_new` AS
SELECT d.id, d.uri, d.kind, t.content_hash
FROM `${PROJECT}.${DATASET}.raw_docs` d
LEFT JOIN `${PROJECT}.${DATASET}.raw_texts` t ON d.id = t.id
LEFT JOIN `${PROJECT}.${DATASET}.emb_jobs_status` s 
  ON d.id = s.id AND s.embedding_type = 'image' AND s.status = 'completed'
WHERE s.id IS NULL AND d.kind = 'image';

-- 6. 임베딩 작업 상태 업데이트 (완료 후)
-- 이 부분은 Python에서 임베딩 생성 완료 후 실행
/*
UPDATE `${PROJECT}.${DATASET}.emb_jobs_status`
SET status = 'completed', updated_at = CURRENT_TIMESTAMP()
WHERE id IN (SELECT id FROM `${PROJECT}.${DATASET}.emb_text_new`);
*/

-- 7. 파티셔닝 및 클러스터링 (대용량 대비)
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.emb_view_t_partitioned`
PARTITION BY DATE(_PARTITIONTIME)
CLUSTER BY id, embedding_type
AS
SELECT 
  id,
  embedding,
  'text' as embedding_type,
  CURRENT_TIMESTAMP() as _PARTITIONTIME
FROM `${PROJECT}.${DATASET}.emb_view_t_vertex`;

-- 8. ORI 파라미터 테이블 생성 (외부화)
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.ori_params` AS
SELECT 
  0.7 AS w,                    -- 의미적 거리 가중치
  0.3 AS tau,                  -- 불일치 임계값
  10 AS top_k,                 -- 상위 K개 결과
  'vertex' AS mode,            -- 실행 모드
  CURRENT_TIMESTAMP() AS created_at;

-- 9. 평가 메트릭 테이블 생성
CREATE OR REPLACE TABLE `${PROJECT}.${DATASET}.eval_metrics` AS
WITH labels AS (
  SELECT 'A100' id, 1 y UNION ALL
  SELECT 'A200', 1 UNION ALL
  SELECT 'A300', 1 UNION ALL
  SELECT 'B100', 0 UNION ALL
  SELECT 'B200', 0 UNION ALL
  SELECT 'C100', 0
),
predictions AS (
  SELECT id, predict, ori FROM `${PROJECT}.${DATASET}.report_ori`
),
metrics AS (
  SELECT 
    COUNT(*) as total_cases,
    SUM(CASE WHEN p.predict = l.y THEN 1 ELSE 0 END) as correct_predictions,
    AVG(CASE WHEN p.predict = l.y THEN 1.0 ELSE 0.0 END) as accuracy,
    -- Precision@K 계산
    SUM(CASE WHEN p.predict = 1 AND l.y = 1 THEN 1 ELSE 0 END) as true_positives,
    SUM(CASE WHEN p.predict = 1 THEN 1 ELSE 0 END) as predicted_positives,
    SUM(CASE WHEN l.y = 1 THEN 1 ELSE 0 END) as actual_positives,
    -- ORI 점수 통계
    AVG(p.ori) as avg_ori_score,
    STDDEV(p.ori) as std_ori_score,
    MIN(p.ori) as min_ori_score,
    MAX(p.ori) as max_ori_score
  FROM predictions p
  LEFT JOIN labels l ON p.id = l.id
)
SELECT 
  total_cases,
  correct_predictions,
  accuracy,
  ROUND(accuracy * 100, 2) as accuracy_percent,
  SAFE_DIVIDE(true_positives, predicted_positives) as precision,
  SAFE_DIVIDE(true_positives, actual_positives) as recall,
  SAFE_DIVIDE(2 * true_positives, predicted_positives + actual_positives) as f1_score,
  avg_ori_score,
  std_ori_score,
  min_ori_score,
  max_ori_score,
  CURRENT_TIMESTAMP() as evaluated_at
FROM metrics;
