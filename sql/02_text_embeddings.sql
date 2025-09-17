
-- 2. 텍스트 임베딩 결과
SELECT 
    id, 
    ARRAY_LENGTH(embedding) as embedding_dim,
    embedding[OFFSET(0)] as first_value,
    embedding[OFFSET(1)] as second_value,
    embedding[OFFSET(2)] as third_value
FROM `gen-lang-client-0790720774.descent_demo.emb_view_t_vertex`
ORDER BY id
LIMIT 5;
        