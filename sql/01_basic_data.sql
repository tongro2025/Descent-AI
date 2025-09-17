
-- 1. 기본 데이터 확인
SELECT id, body, content_hash
FROM `${GCP_PROJECT}.descent_demo.raw_texts`
ORDER BY id
LIMIT 5;
        