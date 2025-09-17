-- Before/After 비교 분석용 SQL
-- 베이스라인: '불일치' 키워드 매칭
WITH baseline AS (
  SELECT id, body,
         IF(REGEXP_CONTAINS(body, r'(불일치|모순|다름)'), 1, 0) AS kw_hit
  FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_texts`
),

-- 우리 방식: 임베딩 결합 벡터에서 질의와 가까운 순
q AS (
  SELECT ML.GENERATE_EMBEDDING(
           MODEL `models.text_embedding`,
           STRUCT('스펙/설명/이미지의 불일치 사례' AS content)
         ).embedding AS qvec
),
ranked AS (
  SELECT s.key, VECTOR_DISTANCE(s.vec, q.qvec) AS score
  FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` s, q
  ORDER BY score ASC
  LIMIT 10
)

SELECT r.key, r.score, b.body, b.kw_hit
FROM ranked r
LEFT JOIN `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` b
ON b.id = r.key
ORDER BY r.score ASC;









