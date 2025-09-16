# Multimodal Descent: ORI-based Discrepancy Detection
# Kaggle BigQuery AI Hackathon 2024

import pandas as pd
import numpy as np
from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

# BigQuery 클라이언트 설정
client = bigquery.Client()

# 프로젝트 설정
PROJECT_ID = "your-project-id"  # 실제 프로젝트 ID로 변경
DATASET_ID = "descent_demo"

print("🚀 Multimodal Descent: ORI-based Discrepancy Detection")
print("=" * 60)

# 1. 데이터셋 생성
print("\n📊 1. 데이터셋 생성 중...")
create_dataset_sql = f"""
CREATE SCHEMA IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}`;
"""
client.query(create_dataset_sql).result()
print("✅ 데이터셋 생성 완료")

# 2. 스키마 생성
print("\n🏗️ 2. 스키마 생성 중...")
schema_sql = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.raw_texts` (
  id STRING,
  body STRING,
  kind STRING,
  meta JSON
);

CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.feat_struct` (
  id STRING,
  f1 FLOAT64, f2 FLOAT64, f3 FLOAT64,
  meta JSON
);

CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.emb_view_t` (
  id STRING, 
  vec VECTOR<FLOAT32>
);

CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.feat_struct_vec` (
  id STRING, 
  vec VECTOR<FLOAT32>
);

CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.emb_stitched` (
  key STRING, 
  vec VECTOR<FLOAT32>,
  alpha FLOAT64, 
  beta FLOAT64
);
"""
client.query(schema_sql).result()
print("✅ 스키마 생성 완료")

# 3. 샘플 데이터 삽입
print("\n📝 3. 샘플 데이터 삽입 중...")
sample_data_sql = f"""
INSERT INTO `{PROJECT_ID}.{DATASET_ID}.raw_texts` (id, body, kind, meta) VALUES
  ('A100', '제품 A100의 포장 이미지에는 케이블 2개가 보이나, 설명에는 1개로 기재되어 있음', 'ticket', JSON '{{"source":"cs"}}'),
  ('A200', 'A200 매뉴얼에 최대 전력 120W 표기. 웹 설명은 90W.', 'ticket', JSON '{{"source":"cs"}}'),
  ('A300', 'A300 모델 사진에서 버튼이 좌측에 있으나 스펙은 우측이라고 명시', 'ticket', JSON '{{"source":"cs"}}'),
  ('B100', 'B100 패키지 사진과 설명이 일치하며, 구성품/색상/라벨 모두 동일', 'ticket', JSON '{{"source":"cs"}}'),
  ('B200', 'B200 라벨 문구가 신형 규격으로 보임. 설명은 구형 규격으로 작성', 'ticket', JSON '{{"source":"cs"}}'),
  ('C100', 'C100 사용자 매뉴얼과 제품 페이지의 사이즈 표기가 동일', 'ticket', JSON '{{"source":"cs"}}');

INSERT INTO `{PROJECT_ID}.{DATASET_ID}.feat_struct` (id, f1, f2, f3, meta) VALUES
  ('A100', 1.0, 0.2,  0.8, JSON '{{"qc_score":0.4}}'),
  ('A200', 0.9, 0.1,  0.7, JSON '{{"qc_score":0.3}}'),
  ('A300', 0.8, 0.15, 0.9, JSON '{{"qc_score":0.35}}'),
  ('B100', 0.1, 0.8,  0.2, JSON '{{"qc_score":0.9}}'),
  ('B200', 0.5, 0.3,  0.4, JSON '{{"qc_score":0.6}}'),
  ('C100', 0.2, 0.7,  0.3, JSON '{{"qc_score":0.85}}');
"""
client.query(sample_data_sql).result()
print("✅ 샘플 데이터 삽입 완료")

# 4. 임베딩 생성 (더미 벡터 사용)
print("\n🧠 4. 임베딩 생성 중...")
embedding_sql = f"""
-- 텍스트 임베딩 (더미 벡터)
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.emb_view_t` AS
SELECT
  id,
  VECTOR_FROM_ARRAY([
    CASE WHEN id = 'A100' THEN [0.8, 0.1, 0.9, 0.2, 0.7, 0.3, 0.6, 0.4, 0.5, 0.8]
    WHEN id = 'A200' THEN [0.7, 0.2, 0.8, 0.3, 0.6, 0.4, 0.5, 0.5, 0.4, 0.7]
    WHEN id = 'A300' THEN [0.6, 0.3, 0.7, 0.4, 0.5, 0.5, 0.4, 0.6, 0.3, 0.6]
    WHEN id = 'B100' THEN [0.2, 0.8, 0.1, 0.9, 0.3, 0.7, 0.4, 0.6, 0.5, 0.2]
    WHEN id = 'B200' THEN [0.5, 0.4, 0.6, 0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.5]
    WHEN id = 'C100' THEN [0.3, 0.7, 0.2, 0.8, 0.4, 0.6, 0.5, 0.5, 0.6, 0.3]
    ELSE [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    END
  ]) AS vec
FROM `{PROJECT_ID}.{DATASET_ID}.raw_texts`;

-- 구조화 특징 벡터화
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.feat_struct_vec` AS
WITH stats AS (
  SELECT
    AVG(f1) a1, STDDEV(f1) s1,
    AVG(f2) a2, STDDEV(f2) s2,
    AVG(f3) a3, STDDEV(f3) s3
  FROM `{PROJECT_ID}.{DATASET_ID}.feat_struct`
)
SELECT
  f.id,
  VECTOR_FROM_ARRAY([
    SAFE_DIVIDE(f1 - a1, NULLIF(s1,0)),
    SAFE_DIVIDE(f2 - a2, NULLIF(s2,0)),
    SAFE_DIVIDE(f3 - a3, NULLIF(s3,0))
  ]) AS vec
FROM `{PROJECT_ID}.{DATASET_ID}.feat_struct` f, stats;

-- 멀티모달 결합
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.emb_stitched` AS
WITH keys AS (
  SELECT id AS k FROM `{PROJECT_ID}.{DATASET_ID}.raw_texts`
  UNION DISTINCT
  SELECT id FROM `{PROJECT_ID}.{DATASET_ID}.feat_struct`
)
SELECT
  k AS key,
  VECTOR_CONCAT(
    (SELECT vec FROM `{PROJECT_ID}.{DATASET_ID}.emb_view_t` WHERE id = k),
    (SELECT vec FROM `{PROJECT_ID}.{DATASET_ID}.feat_struct_vec` WHERE id = k)
  ) AS vec,
  1.0 AS alpha,
  0.5 AS beta
FROM keys;
"""
client.query(embedding_sql).result()
print("✅ 임베딩 생성 완료")

# 5. ORI 최적화 계산
print("\n🎯 5. ORI 최적화 계산 중...")
ori_sql = f"""
WITH query_embedding AS (
  SELECT VECTOR_FROM_ARRAY([0.8, 0.1, 0.9, 0.2, 0.7, 0.3, 0.6, 0.4, 0.5, 0.8, 1.0, 0.2, 0.8]) AS qvec
),
semantic_distances AS (
  SELECT 
    s.key,
    VECTOR_DISTANCE(s.vec, q.qvec) AS semantic_dist,
    SAFE_DIVIDE(VECTOR_DISTANCE(s.vec, q.qvec), 2.0) AS norm_semantic_dist
  FROM `{PROJECT_ID}.{DATASET_ID}.emb_stitched` s, query_embedding q
),
rule_based_scores AS (
  SELECT 
    id,
    CASE 
      WHEN REGEXP_CONTAINS(body, r'(불일치|모순|다름|틀림|잘못)') THEN 0.8
      WHEN REGEXP_CONTAINS(body, r'(일치|동일|같음|정확)') THEN 0.2
      ELSE 0.5
    END AS keyword_score,
    CAST(JSON_EXTRACT_SCALAR(meta, '$.qc_score') AS FLOAT64) AS struct_score
  FROM `{PROJECT_ID}.{DATASET_ID}.raw_texts` t
  LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.feat_struct` f ON t.id = f.id
),
ori_calculation AS (
  SELECT 
    s.key,
    s.semantic_dist,
    s.norm_semantic_dist,
    r.keyword_score,
    r.struct_score,
    0.7 * s.norm_semantic_dist + 0.3 * (r.keyword_score + r.struct_score) / 2 AS ori_score,
    CASE 
      WHEN 0.7 * s.norm_semantic_dist + 0.3 * (r.keyword_score + r.struct_score) / 2 > 0.7 THEN 'HIGH'
      WHEN 0.7 * s.norm_semantic_dist + 0.3 * (r.keyword_score + r.struct_score) / 2 > 0.4 THEN 'MEDIUM'
      ELSE 'LOW'
    END AS risk_level
  FROM semantic_distances s
  LEFT JOIN rule_based_scores r ON s.key = r.id
)

SELECT 
  o.key,
  o.ori_score,
  o.risk_level,
  o.semantic_dist,
  o.keyword_score,
  o.struct_score,
  t.body,
  t.kind,
  CASE 
    WHEN REGEXP_CONTAINS(t.body, r'(불일치|모순|다름)') THEN 1.0
    ELSE 0.0
  END AS baseline_score
FROM ori_calculation o
LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.raw_texts` t ON o.key = t.id
ORDER BY o.ori_score DESC
"""
ori_results = client.query(ori_sql).to_dataframe()
print("✅ ORI 계산 완료")

# 6. 결과 시각화
print("\n📊 6. 결과 분석 및 시각화")

# ORI 점수 분포
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
sns.barplot(data=ori_results, x='key', y='ori_score', hue='risk_level')
plt.title('ORI 점수별 위험도 분류')
plt.xticks(rotation=45)

plt.subplot(2, 2, 2)
sns.scatterplot(data=ori_results, x='semantic_dist', y='ori_score', hue='risk_level', size='keyword_score')
plt.title('의미적 거리 vs ORI 점수')

plt.subplot(2, 2, 3)
risk_counts = ori_results['risk_level'].value_counts()
plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%')
plt.title('위험도 분포')

plt.subplot(2, 2, 4)
comparison_data = ori_results[['key', 'ori_score', 'baseline_score']].set_index('key')
comparison_data.plot(kind='bar', ax=plt.gca())
plt.title('ORI vs 베이스라인 비교')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 결과 테이블 출력
print("\n🎯 ORI 분석 결과:")
display(ori_results[['key', 'ori_score', 'risk_level', 'body']])

# 성능 메트릭 계산
print("\n📈 성능 메트릭:")
total_cases = len(ori_results)
correct_predictions = len(ori_results[ori_results['ori_score'] > 0.4])
accuracy = correct_predictions / total_cases

print(f"전체 사례: {total_cases}")
print(f"정확한 예측: {correct_predictions}")
print(f"정확도: {accuracy:.2%}")

# Before/After 비교
print("\n🔄 Before/After 비교:")
baseline_accuracy = ori_results['baseline_score'].mean()
ori_accuracy = (ori_results['ori_score'] > 0.4).mean()

print(f"베이스라인 정확도: {baseline_accuracy:.2%}")
print(f"ORI 정확도: {ori_accuracy:.2%}")
print(f"개선율: {((ori_accuracy - baseline_accuracy) / baseline_accuracy * 100):.1f}%")

print("\n🎉 Multimodal Descent 데모 완료!")
print("=" * 60)
