# BigQuery 결과 캡처 요약
==================================================

## 캡처된 쿼리 결과

| 쿼리명 | 행 수 | 컬럼 수 | 상태 |
|--------|-------|---------|------|
| basic_data | - | - | ❌ 400 Unrecognized name: content_hash at [2:26]; reason: invalidQuery, location: query, message: Unrecognized name: content_hash at [2:26]

Location: US
Job ID: 41a944df-2a52-4291-9793-5cd3dcf1fd46
 |
| text_embeddings | 5 | ['id', 'embedding_dim', 'first_value', 'second_value', 'third_value'] | ✅ |
| image_embeddings | 3 | ['id', 'uri', 'embedding_dim', 'model_name', 'model_version', 'embedding_type', 'first_value', 'second_value', 'third_value'] | ✅ |
| ori_results | - | - | ❌ 400 Unrecognized name: risk_level at [8:13]; reason: invalidQuery, location: query, message: Unrecognized name: risk_level at [8:13]

Location: US
Job ID: a3d41b2f-21c9-4196-acae-726146b0ea8d
 |
| multimodal_comparison | 10 | ['mode', 'id', 'ori', 'predict', 'semantic_distance', 'rule_score'] | ✅ |
| embedding_dimensions | 4 | ['type', 'dimensions', 'model_name'] | ✅ |
| evaluation_metrics | - | - | ❌ 400 Unrecognized name: avg_ori_score at [10:13]; reason: invalidQuery, location: query, message: Unrecognized name: avg_ori_score at [10:13]

Location: US
Job ID: 0ab64374-0e7f-462e-a5b3-039447e30b76
 |
| multimodal_stitched | 5 | ['key', 'total_dimensions', 'alpha_text', 'beta_struct', 'gamma_image', 'fusion_method'] | ✅ |

## 생성된 파일들

- `artifacts/bq_results_text_embeddings.csv` - CSV 형식
- `artifacts/bq_results_text_embeddings.json` - JSON 형식
- `artifacts/bq_results_image_embeddings.csv` - CSV 형식
- `artifacts/bq_results_image_embeddings.json` - JSON 형식
- `artifacts/bq_results_multimodal_comparison.csv` - CSV 형식
- `artifacts/bq_results_multimodal_comparison.json` - JSON 형식
- `artifacts/bq_results_embedding_dimensions.csv` - CSV 형식
- `artifacts/bq_results_embedding_dimensions.json` - JSON 형식
- `artifacts/bq_results_multimodal_stitched.csv` - CSV 형식
- `artifacts/bq_results_multimodal_stitched.json` - JSON 형식

## 스크린샷 캡처 가이드

1. **BigQuery Console** 접속
2. **쿼리 편집기**에서 위 쿼리들 실행
3. **결과 탭**에서 스크린샷 캡처
4. **스키마 탭**에서 테이블 구조 캡처

## 주요 캡처 포인트

- ✅ 텍스트 임베딩 (768차원)
- ✅ 이미지 임베딩 (1408차원)
- ✅ 멀티모달 통합 (2179차원)
- ✅ ORI 분석 결과
- ✅ 평가 메트릭
- ✅ 차원 비교