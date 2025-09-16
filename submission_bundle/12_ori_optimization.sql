-- ORI (Outlier Risk Index) 최적화 계산
-- w=0.7 (의미적 거리 가중치), τ=0.3 (임계값)
WITH query_embedding AS (
  SELECT ML.GENERATE_EMBEDDING(
    MODEL `models.textembedding-gecko@001`,
    STRUCT('스펙과 이미지의 불일치 사례' AS content)
  ).embedding AS qvec
),
semantic_distances AS (
  SELECT 
    s.key,
    VECTOR_DISTANCE(s.vec, q.qvec) AS semantic_dist,
    -- 정규화된 의미적 거리 (0-1 범위)
    SAFE_DIVIDE(VECTOR_DISTANCE(s.vec, q.qvec), 2.0) AS norm_semantic_dist
  FROM `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched` s, query_embedding q
),
rule_based_scores AS (
  SELECT 
    id,
    -- 키워드 기반 점수 (불일치 관련 키워드)
    CASE 
      WHEN REGEXP_CONTAINS(body, r'(불일치|모순|다름|틀림|잘못)') THEN 0.8
      WHEN REGEXP_CONTAINS(body, r'(일치|동일|같음|정확)') THEN 0.2
      ELSE 0.5
    END AS keyword_score,
    -- 구조적 특징 기반 점수 (qc_score 활용)
    CAST(JSON_EXTRACT_SCALAR(meta, '$.qc_score') AS FLOAT64) AS struct_score
  FROM `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` t
  LEFT JOIN `${GCP_PROJECT}.${BQ_DATASET}.feat_struct` f ON t.id = f.id
),
ori_calculation AS (
  SELECT 
    s.key,
    s.semantic_dist,
    s.norm_semantic_dist,
    r.keyword_score,
    r.struct_score,
    -- ORI 공식: w * semantic_distance + (1-w) * rule_score
    -- w=0.7, τ=0.3 적용
    0.7 * s.norm_semantic_dist + 0.3 * (r.keyword_score + r.struct_score) / 2 AS ori_score,
    -- 위험도 분류
    CASE 
      WHEN 0.7 * s.norm_semantic_dist + 0.3 * (r.keyword_score + r.struct_score) / 2 > 0.7 THEN 'HIGH'
      WHEN 0.7 * s.norm_semantic_dist + 0.3 * (r.keyword_score + r.struct_score) / 2 > 0.4 THEN 'MEDIUM'
      ELSE 'LOW'
    END AS risk_level
  FROM semantic_distances s
  LEFT JOIN rule_based_scores r ON s.key = r.id
)

SELECT 
  o.key,
  o.ori_score,
  o.risk_level,
  o.semantic_dist,
  o.keyword_score,
  o.struct_score,
  t.body,
  t.kind,
  -- Before/After 비교를 위한 베이스라인 점수
  CASE 
    WHEN REGEXP_CONTAINS(t.body, r'(불일치|모순|다름)') THEN 1.0
    ELSE 0.0
  END AS baseline_score
FROM ori_calculation o
LEFT JOIN `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` t ON o.key = t.id
ORDER BY o.ori_score DESC;
