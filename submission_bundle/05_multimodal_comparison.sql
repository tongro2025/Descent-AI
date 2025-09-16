
-- 5. 멀티모달 비교
SELECT 
    'text' as mode, 
    id, 
    ori, 
    predict,
    semantic_distance,
    rule_score
FROM `gen-lang-client-0790720774.descent_demo.report_ori`
UNION ALL
SELECT 
    'multimodal' as mode, 
    id, 
    ori, 
    predict,
    semantic_distance,
    rule_score
FROM `gen-lang-client-0790720774.descent_demo.report_ori_mm`
ORDER BY mode, ori DESC
LIMIT 10;
        