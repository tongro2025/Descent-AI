-- 샘플 데이터 삽입용 SQL 파일
-- 텍스트(이슈/설명) 예시 6건
INSERT INTO `${GCP_PROJECT}.${BQ_DATASET}.raw_texts` (id, body, kind, meta) VALUES
  ('A100', '제품 A100의 포장 이미지에는 케이블 2개가 보이나, 설명에는 1개로 기재되어 있음', 'ticket', JSON '{"source":"cs"}'),
  ('A200', 'A200 매뉴얼에 최대 전력 120W 표기. 웹 설명은 90W.', 'ticket', JSON '{"source":"cs"}'),
  ('A300', 'A300 모델 사진에서 버튼이 좌측에 있으나 스펙은 우측이라고 명시', 'ticket', JSON '{"source":"cs"}'),
  ('B100', 'B100 패키지 사진과 설명이 일치하며, 구성품/색상/라벨 모두 동일', 'ticket', JSON '{"source":"cs"}'),
  ('B200', 'B200 라벨 문구가 신형 규격으로 보임. 설명은 구형 규격으로 작성', 'ticket', JSON '{"source":"cs"}'),
  ('C100', 'C100 사용자 매뉴얼과 제품 페이지의 사이즈 표기가 동일', 'ticket', JSON '{"source":"cs"}');

-- 구조화 특징(간단 3컬럼) 예시 6건
INSERT INTO `${GCP_PROJECT}.${BQ_DATASET}.feat_struct` (id, f1, f2, f3, meta) VALUES
  ('A100', 1.0, 0.2,  0.8, JSON '{"qc_score":0.4}'),
  ('A200', 0.9, 0.1,  0.7, JSON '{"qc_score":0.3}'),
  ('A300', 0.8, 0.15, 0.9, JSON '{"qc_score":0.35}'),
  ('B100', 0.1, 0.8,  0.2, JSON '{"qc_score":0.9}'),
  ('B200', 0.5, 0.3,  0.4, JSON '{"qc_score":0.6}'),
  ('C100', 0.2, 0.7,  0.3, JSON '{"qc_score":0.85}');




