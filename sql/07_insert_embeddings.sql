-- 임베딩 데이터 삽입
-- 텍스트 임베딩 삽입
INSERT INTO `${GCP_PROJECT}.descent_demo.text_embeddings` (id, text, embedding)
SELECT 
  id,
  body as text,
  CASE 
    WHEN id = 'A100' THEN [0.1, 0.2, 0.3, 0.4, 0.5]
    WHEN id = 'A200' THEN [0.2, 0.3, 0.4, 0.5, 0.6]
    WHEN id = 'A300' THEN [0.3, 0.4, 0.5, 0.6, 0.7]
    WHEN id = 'B100' THEN [0.8, 0.9, 0.1, 0.2, 0.3]
    WHEN id = 'B200' THEN [0.5, 0.6, 0.7, 0.8, 0.9]
    WHEN id = 'C100' THEN [0.9, 0.1, 0.2, 0.3, 0.4]
  END as embedding
FROM `${GCP_PROJECT}.descent_demo.raw_texts`;

-- 구조화 특징 벡터 삽입
INSERT INTO `${GCP_PROJECT}.descent_demo.struct_embeddings` (id, features)
SELECT 
  id,
  [f1, f2, f3] as features
FROM `${GCP_PROJECT}.descent_demo.feat_struct`;

-- 통합 임베딩 생성 (텍스트 + 구조화 특징 결합)
INSERT INTO `${GCP_PROJECT}.descent_demo.combined_embeddings` (id, text_embedding, struct_embedding, combined_embedding)
SELECT 
  t.id,
  t.embedding as text_embedding,
  s.features as struct_embedding,
  ARRAY_CONCAT(t.embedding, s.features) as combined_embedding
FROM `${GCP_PROJECT}.descent_demo.text_embeddings` t
JOIN `${GCP_PROJECT}.descent_demo.struct_embeddings` s
ON t.id = s.id;












