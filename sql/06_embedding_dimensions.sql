
-- 6. 임베딩 차원 비교
WITH text_dims AS (
    SELECT 'text' as type, ARRAY_LENGTH(embedding) as dimensions, 'Vertex AI text-embedding-005' as model_name
    FROM `${GCP_PROJECT}.descent_demo.emb_view_t_vertex`
    LIMIT 1
),
image_dims AS (
    SELECT 'image' as type, ARRAY_LENGTH(embedding) as dimensions, model_name
    FROM `${GCP_PROJECT}.descent_demo.emb_view_i_real`
    LIMIT 1
),
struct_dims AS (
    SELECT 'struct' as type, ARRAY_LENGTH(embedding) as dimensions, 'Z-score normalized' as model_name
    FROM `${GCP_PROJECT}.descent_demo.feat_struct_vec`
    LIMIT 1
),
multimodal_dims AS (
    SELECT 'multimodal' as type, AVG(total_dimensions) as dimensions, 'Concatenated' as model_name
    FROM `${GCP_PROJECT}.descent_demo.emb_stitched_real`
    LIMIT 1
)
SELECT * FROM text_dims
UNION ALL
SELECT * FROM image_dims
UNION ALL
SELECT * FROM struct_dims
UNION ALL
SELECT * FROM multimodal_dims
ORDER BY type;
        