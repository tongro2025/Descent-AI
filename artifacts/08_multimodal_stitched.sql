
-- 8. 멀티모달 통합 결과
SELECT 
    key,
    total_dimensions,
    alpha_text,
    beta_struct,
    gamma_image,
    fusion_method
FROM `gen-lang-client-0790720774.descent_demo.emb_stitched_real`
ORDER BY total_dimensions DESC
LIMIT 5;
        