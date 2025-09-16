-- Vertex AI 기반 ORI 지수 및 리포트 뷰 생성

-- 라벨 테이블 생성
CREATE OR REPLACE TABLE `${GCP_PROJECT}.${BQ_DATASET}.labels` AS
SELECT 'A100' id, 1 y UNION ALL
SELECT 'A200', 1 UNION ALL
SELECT 'A300', 1 UNION ALL
SELECT 'B100', 0 UNION ALL
SELECT 'B200', 0 UNION ALL
SELECT 'C100', 0;

-- 코사인 거리 계산용 UDF
CREATE TEMP FUNCTION cosine_dist(a ARRAY<FLOAT64>, b ARRAY<FLOAT64>) AS (
  1.0 - SAFE_DIVIDE(
    (SELECT SUM(ax*bx) FROM UNNEST(a) ax WITH OFFSET i
     JOIN UNNEST(b) bx WITH OFFSET j ON i=j),
    SQRT((SELECT SUM(x*x) FROM UNNEST(a) x)) * SQRT((SELECT SUM(x*x) FROM UNNEST(b) x))
  )
);

-- ORI 계산용 뷰
CREATE OR REPLACE VIEW `${GCP_PROJECT}.${BQ_DATASET}.report_ori` AS
WITH q AS (
  -- 질의 벡터: A100 불일치 사례를 기준으로 사용
  SELECT (SELECT embedding FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t_norm` WHERE id='A100') AS qvec
),
scores AS (
  SELECT s.key AS id,
         cosine_dist(s.embedding, (SELECT qvec FROM q)) AS d,
         IF(REGEXP_CONTAINS(t.body, r'(불일치|모순|상이|다름)'), 1.0, 0.0) AS rule_score
  FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` s
  LEFT JOIN `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` t ON t.id=s.key
),
norm AS (
  SELECT id, rule_score,
         (d - MIN(d) OVER()) / NULLIF(MAX(d) OVER() - MIN(d) OVER(),0) AS dz
  FROM scores
)
SELECT id,
       0.7 * dz + 0.3 * (1.0 - rule_score) AS ori,
       CASE WHEN (0.7 * dz + 0.3 * (1.0 - rule_score)) >= 0.3 THEN 1 ELSE 0 END AS predict,
       dz AS semantic_distance,
       rule_score,
       t.body
FROM norm
LEFT JOIN `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` t ON norm.id = t.id
ORDER BY ori DESC;

-- Before/After 비교 뷰
CREATE OR REPLACE VIEW `${GCP_PROJECT}.${BQ_DATASET}.report_before_after` AS
WITH q AS (
  SELECT (SELECT embedding FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_view_t_norm` WHERE id='A100') AS qvec
),
ranked AS (
  SELECT s.key AS id,
         cosine_dist(s.embedding, (SELECT qvec FROM q)) AS distance,
         ROW_NUMBER() OVER (ORDER BY cosine_dist(s.embedding, (SELECT qvec FROM q)) ASC) AS rk
  FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` s
),
baseline AS (
  SELECT id,
         IF(REGEXP_CONTAINS(body, r'(불일치|모순|상이|다름)'), 1, 0) AS kw_hit
  FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_texts`
)
SELECT r.rk, r.id, r.distance AS vec_score, b.kw_hit,
       t.body
FROM ranked r
LEFT JOIN baseline b USING(id)
LEFT JOIN `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` t ON r.id = t.id
ORDER BY r.rk;
