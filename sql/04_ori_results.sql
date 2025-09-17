
-- 4. ORI 분석 결과
SELECT 
    id, 
    ori, 
    predict, 
    semantic_distance, 
    rule_score, 
    risk_level,
    SUBSTR(body, 1, 50) as content_preview
FROM `${GCP_PROJECT}.descent_demo.report_ori`
ORDER BY ori DESC
LIMIT 10;
        