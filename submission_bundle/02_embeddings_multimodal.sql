-- 멀티모달 임베딩 생성 (이미지/PDF)
-- GCS에 파일 업로드 후 Object Table 생성 필요

-- 이미지/PDF 임베딩 생성
CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.emb_view_i` AS
SELECT
  uri,
  ML.GENERATE_EMBEDDING(
    MODEL `models.multimodal_embedding`,
    STRUCT(ref AS content)
  ).embedding AS vec
FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_docs`
WHERE kind IN ('image','pdf');

-- 멀티모달 결합 (텍스트 + 이미지 + 구조화 특징)
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
    -- 이미지 임베딩 (있는 경우만)
    (SELECT vec FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_i` WHERE uri LIKE CONCAT('%', k, '%')),
    (SELECT vec FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec` WHERE id = k)
  ) AS vec,
  1.0 AS alpha,
  0.5 AS beta
FROM keys;
