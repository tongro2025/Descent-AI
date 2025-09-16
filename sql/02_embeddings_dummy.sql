-- 더미 벡터 임베딩 (데모용)
-- USE_REAL_EMBEDDINGS=false일 때 사용

CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t` AS
SELECT
  id,
  VECTOR_FROM_ARRAY([
    -- A100: 불일치 사례 (높은 위험도)
    CASE WHEN id = 'A100' THEN [0.8, 0.1, 0.9, 0.2, 0.7, 0.3, 0.6, 0.4, 0.5, 0.8]
    -- A200: 불일치 사례 (중간 위험도)  
    WHEN id = 'A200' THEN [0.7, 0.2, 0.8, 0.3, 0.6, 0.4, 0.5, 0.5, 0.4, 0.7]
    -- A300: 불일치 사례 (중간 위험도)
    WHEN id = 'A300' THEN [0.6, 0.3, 0.7, 0.4, 0.5, 0.5, 0.4, 0.6, 0.3, 0.6]
    -- B100: 일치 사례 (낮은 위험도)
    WHEN id = 'B100' THEN [0.2, 0.8, 0.1, 0.9, 0.3, 0.7, 0.4, 0.6, 0.5, 0.2]
    -- B200: 불일치 사례 (중간 위험도)
    WHEN id = 'B200' THEN [0.5, 0.4, 0.6, 0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.5]
    -- C100: 일치 사례 (낮은 위험도)
    WHEN id = 'C100' THEN [0.3, 0.7, 0.2, 0.8, 0.4, 0.6, 0.5, 0.5, 0.6, 0.3]
    ELSE [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    END
  ]) AS vec
FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_texts`;

-- 구조화 특징 → z-score → 벡터
CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec` AS
WITH stats AS (
  SELECT
    AVG(f1) a1, STDDEV(f1) s1,
    AVG(f2) a2, STDDEV(f2) s2,
    AVG(f3) a3, STDDEV(f3) s3
  FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct`
)
SELECT
  f.id,
  VECTOR_FROM_ARRAY([
    SAFE_DIVIDE(f1 - a1, NULLIF(s1,0)),
    SAFE_DIVIDE(f2 - a2, NULLIF(s2,0)),
    SAFE_DIVIDE(f3 - a3, NULLIF(s3,0))
  ]) AS vec
FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct` f, stats;

-- 스티칭: T ⊕ S (텍스트 + 구조화 특징)
CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` AS
WITH keys AS (
  SELECT id AS k FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_texts`
  UNION DISTINCT
  SELECT id FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct`
)
SELECT
  k AS key,
  VECTOR_CONCAT(
    (SELECT vec FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t` WHERE id = k),
    (SELECT vec FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec` WHERE id = k)
  ) AS vec,
  1.0 AS alpha,
  0.5 AS beta
FROM keys;
