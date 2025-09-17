-- 원천 테이블
CREATE SCHEMA IF NOT EXISTS `${GCP_PROJECT}.descent_demo`;
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.raw_docs` (
  ref OBJECTREF,
  uri STRING,
  kind STRING,
  meta JSON
);
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.raw_texts` (
  id STRING,
  body STRING,
  kind STRING,
  meta JSON
);
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.feat_struct` (
  id STRING,
  f1 FLOAT64, f2 FLOAT64, f3 FLOAT64,
  meta JSON
);

-- 임베딩/결합
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.emb_view_t` (
  id STRING, vec VECTOR<FLOAT32>
);
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.emb_view_i` (
  uri STRING, vec VECTOR<FLOAT32>
);
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.feat_struct_vec` (
  id STRING, vec VECTOR<FLOAT32>
);
CREATE OR REPLACE TABLE `${GCP_PROJECT}.descent_demo.emb_stitched` (
  key STRING, vec VECTOR<FLOAT32>,
  alpha FLOAT64, beta FLOAT64
);

참고: 이미지/PDF는 GCS에 올려 Object Table로 등록(콘솔/CLI). 초기에는 텍스트만 먼저 돌려도 됨.
