-- 로컬 시뮬레이션용 SQL (빌링 없이 실행 가능)
-- 현재 데이터로 간단한 유사도 검색 시뮬레이션

-- 1. 키워드 매칭 베이스라인
WITH baseline AS (
  SELECT 
    id, 
    body,
    IF(REGEXP_CONTAINS(body, r'(불일치|모순|다름|다르|틀리)'), 1, 0) AS kw_hit,
    CASE 
      WHEN REGEXP_CONTAINS(body, r'(불일치|모순|다름|다르|틀리)') THEN 1.0
      ELSE 0.0
    END as kw_score
  FROM `gen-lang-client-0790720774.descent_demo.raw_texts`
),

-- 2. 구조화 특징 기반 유사도 (수치적 유사도)
struct_similarity AS (
  SELECT 
    id,
    f1, f2, f3,
    -- 불일치 사례는 f1이 높고 f2가 낮은 패턴
    ABS(f1 - 1.0) + ABS(f2 - 0.2) + ABS(f3 - 0.8) as a100_distance,
    ABS(f1 - 0.9) + ABS(f2 - 0.1) + ABS(f3 - 0.7) as a200_distance,
    ABS(f1 - 0.8) + ABS(f2 - 0.15) + ABS(f3 - 0.9) as a300_distance,
    -- 가장 가까운 불일치 사례와의 거리
    LEAST(
      ABS(f1 - 1.0) + ABS(f2 - 0.2) + ABS(f3 - 0.8),
      ABS(f1 - 0.9) + ABS(f2 - 0.1) + ABS(f3 - 0.7),
      ABS(f1 - 0.8) + ABS(f2 - 0.15) + ABS(f3 - 0.9)
    ) as min_distance
  FROM `gen-lang-client-0790720774.descent_demo.feat_struct`
),

-- 3. 텍스트 길이 기반 유사도 (간단한 휴리스틱)
text_similarity AS (
  SELECT 
    id,
    body,
    LENGTH(body) as text_length,
    -- 불일치 사례는 보통 긴 설명을 가짐
    CASE 
      WHEN LENGTH(body) > 50 THEN 0.8
      WHEN LENGTH(body) > 30 THEN 0.5
      ELSE 0.2
    END as length_score
  FROM `gen-lang-client-0790720774.descent_demo.raw_texts`
)

-- 4. 통합 점수 계산
SELECT 
  b.id,
  b.body,
  b.kw_hit,
  b.kw_score,
  s.min_distance,
  t.length_score,
  -- 가중 평균으로 최종 점수 계산
  (b.kw_score * 0.4 + (1.0 - s.min_distance) * 0.3 + t.length_score * 0.3) as combined_score,
  CASE 
    WHEN b.kw_hit = 1 THEN '키워드 매칭'
    WHEN (1.0 - s.min_distance) > 0.7 THEN '구조화 특징 유사도'
    WHEN t.length_score > 0.6 THEN '텍스트 길이 기반'
    ELSE '낮은 유사도'
  END as detection_method
FROM baseline b
JOIN struct_similarity s ON b.id = s.id
JOIN text_similarity t ON b.id = t.id
ORDER BY combined_score DESC;








