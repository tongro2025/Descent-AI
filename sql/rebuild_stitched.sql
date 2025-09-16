-- Vertex AI 기반 스티칭 재생성
-- L2 정규화 및 통합 임베딩 생성

-- 텍스트 임베딩 L2 정규화 뷰
CREATE OR REPLACE VIEW `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t_norm` AS
SELECT id,
  (SELECT ARRAY(
     SELECT x/NULLIF(SQRT(SUM(y*y) OVER()),0) FROM UNNEST(embedding) x WITH OFFSET
     WINDOW w AS ()
  )) AS embedding
FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t_vertex`;

-- 구조화 특징 벡터화 및 정규화
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
  [
    SAFE_DIVIDE(f1 - a1, NULLIF(s1,0)),
    SAFE_DIVIDE(f2 - a2, NULLIF(s2,0)),
    SAFE_DIVIDE(f3 - a3, NULLIF(s3,0))
  ] AS embedding
FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct` f, stats;

-- 구조화 특징 L2 정규화 뷰
CREATE OR REPLACE VIEW `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec_norm` AS
SELECT id,
  (SELECT ARRAY(
     SELECT x/NULLIF(SQRT(SUM(y*y) OVER()),0) FROM UNNEST(embedding) x WITH OFFSET
     WINDOW w AS ()
  )) AS embedding
FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec`;

-- 스티칭 테이블 재작성 (Vertex AI 기반)
CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` AS
WITH keys AS (
  SELECT id AS k FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_texts`
  UNION DISTINCT
  SELECT id FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec`
)
SELECT
  k AS key,
  ARRAY_CONCAT(
    (SELECT embedding FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t_norm` WHERE id=k),
    (SELECT embedding FROM `${GCP_PROJECT}.${BQ_DATASET}.feat_struct_vec_norm` WHERE id=k)
  ) AS embedding,
  1.0 AS alpha, 
  0.5 AS beta
FROM keys;
