-- 벡터 검색 테스트
-- 1. 텍스트 임베딩 검색 (불일치 사례 찾기)
SELECT 
  id,
  text,
  distance
FROM VECTOR_SEARCH(
  TABLE `gen-lang-client-0790720774.descent_demo.text_embeddings`,
  'embedding',
  [0.1, 0.2, 0.3, 0.4, 0.5], -- A100과 유사한 쿼리
  top_k => 3,
  distance_type => 'COSINE'
);

-- 2. 구조화 특징 검색
SELECT 
  id,
  features,
  distance
FROM VECTOR_SEARCH(
  TABLE `gen-lang-client-0790720774.descent_demo.struct_embeddings`,
  'features',
  [1.0, 0.2, 0.8], -- A100의 특징과 유사한 쿼리
  top_k => 3,
  distance_type => 'COSINE'
);

-- 3. 통합 임베딩 검색 (멀티모달)
SELECT 
  id,
  text_embedding,
  struct_embedding,
  combined_embedding,
  distance
FROM VECTOR_SEARCH(
  TABLE `gen-lang-client-0790720774.descent_demo.combined_embeddings`,
  'combined_embedding',
  [0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 0.2, 0.8], -- 텍스트 + 구조화 특징 결합
  top_k => 5,
  distance_type => 'COSINE'
);

