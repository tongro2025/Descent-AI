-- 벡터 인덱스 생성
-- 텍스트 임베딩용 IVF 인덱스
CREATE VECTOR INDEX text_embeddings_ivf
ON `gen-lang-client-0790720774.descent_demo.text_embeddings`(embedding)
OPTIONS(index_type = 'IVF', distance_type = 'COSINE');

-- 구조화 특징용 IVF 인덱스
CREATE VECTOR INDEX struct_embeddings_ivf
ON `gen-lang-client-0790720774.descent_demo.struct_embeddings`(features)
OPTIONS(index_type = 'IVF', distance_type = 'COSINE');

-- 통합 임베딩용 TreeAH 인덱스 (더 복잡한 벡터에 적합)
CREATE VECTOR INDEX combined_embeddings_treeah
ON `gen-lang-client-0790720774.descent_demo.combined_embeddings`(combined_embedding)
OPTIONS(index_type = 'TREE_AH', distance_type = 'COSINE');







