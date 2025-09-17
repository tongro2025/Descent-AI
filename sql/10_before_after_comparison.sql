-- Before/After 비교 분석
-- 베이스라인: 키워드 매칭
WITH baseline AS (
  SELECT 
    id, 
    body,
    IF(REGEXP_CONTAINS(body, r'(불일치|모순|다름|다르|틀리)'), 1, 0) AS kw_hit
  FROM `gen-lang-client-0790720774.descent_demo.raw_texts`
),

-- 우리 방식: 벡터 검색
vector_search AS (
  SELECT 
    id,
    text,
    distance
  FROM VECTOR_SEARCH(
    TABLE `gen-lang-client-0790720774.descent_demo.text_embeddings`,
    'embedding',
    [0.1, 0.2, 0.3, 0.4, 0.5], -- "불일치 사례"와 유사한 쿼리 벡터
    top_k => 6,
    distance_type => 'COSINE'
  )
)

-- 결과 비교
SELECT 
  v.id,
  v.text,
  v.distance as vector_score,
  b.kw_hit,
  CASE 
    WHEN b.kw_hit = 1 THEN '키워드 매칭'
    WHEN v.distance < 0.3 THEN '벡터 검색 (높은 유사도)'
    WHEN v.distance < 0.6 THEN '벡터 검색 (중간 유사도)'
    ELSE '벡터 검색 (낮은 유사도)'
  END as search_method,
  CASE 
    WHEN b.kw_hit = 0 AND v.distance < 0.5 THEN '벡터 검색 우위'
    WHEN b.kw_hit = 1 AND v.distance > 0.7 THEN '키워드 매칭 우위'
    ELSE '동등'
  END as comparison
FROM vector_search v
LEFT JOIN baseline b ON v.id = b.id
ORDER BY v.distance ASC;




