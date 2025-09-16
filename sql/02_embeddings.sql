-- 텍스트 임베딩 (BigQuery AI 모델 사용)
CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t` AS
SELECT
  id,
  ML.GENERATE_EMBEDDING(
    MODEL `models.text_embedding`,
    STRUCT(body AS content)
  ).embedding AS vec
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

-- (선택) 이미지/PDF 임베딩: ObjectRef가 준비되면 주석 해제
-- CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.emb_view_i` AS
-- SELECT
--   uri,
--   ML.GENERATE_EMBEDDING(
--     MODEL `models.multimodal_embedding`,
--     STRUCT(ref AS content)
--   ).embedding AS vec
-- FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_docs`
-- WHERE kind IN ('image','pdf');

-- 스티칭: T ⊕ I ⊕ S (I가 없으면 T ⊕ S만)
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
    -- (SELECT vec FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_i` WHERE uri LIKE CONCAT('%', k, '%')),
    (SELECT vec FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec` WHERE id = k)
  ) AS vec,
  1.0 AS alpha,
  0.5 AS beta
FROM keys;

