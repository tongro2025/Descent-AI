
-- 7. 평가 메트릭
SELECT 
    total_cases,
    correct_predictions,
    accuracy,
    accuracy_percent,
    precision,
    recall,
    f1_score,
    avg_ori_score,
    std_ori_score,
    min_ori_score,
    max_ori_score,
    evaluated_at
FROM `${GCP_PROJECT}.descent_demo.eval_metrics`;
        