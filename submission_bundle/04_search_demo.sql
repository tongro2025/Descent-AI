WITH q AS (
  SELECT ML.GENERATE_EMBEDDING(
    MODEL `models.text_embedding`,
    STRUCT(@query AS content)
  ).embedding AS qvec
)
SELECT key,
       VECTOR_DISTANCE(s.vec, q.qvec) AS score
FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` s, q
ORDER BY score ASC
LIMIT @top_k;

