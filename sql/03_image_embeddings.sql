
-- 3. 이미지 임베딩 결과 (실제 Vertex AI)
SELECT 
    id, 
    uri,
    embedding_dim,
    model_name,
    model_version,
    embedding_type,
    embedding[OFFSET(0)] as first_value,
    embedding[OFFSET(1)] as second_value,
    embedding[OFFSET(2)] as third_value
FROM `${GCP_PROJECT}.descent_demo.emb_view_i_real`
ORDER BY id
LIMIT 5;
        