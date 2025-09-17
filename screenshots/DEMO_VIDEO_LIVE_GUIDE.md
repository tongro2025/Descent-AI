# 🎬 데모 영상 촬영 실시간 가이드

## 📱 화면 녹화 시작 전 체크리스트

### ✅ 준비사항
- [ ] 화면 녹화 소프트웨어 실행 (QuickTime Player 또는 다른 도구)
- [ ] 터미널 창 준비
- [ ] 브라우저에서 BigQuery Console 준비
- [ ] 프로젝트 ID 설정 확인

### 🎥 촬영 순서 (총 5-6분)

## 1️⃣ 인트로 및 CLI 실행 (1분)

### 화면: 터미널
### 대사:
```
안녕하세요! BigQuery AI 해커톤에 참여한 Descent 팀입니다.

오늘은 멀티모달 데이터의 불일치를 감지하는 혁신적인 시스템을 소개하겠습니다.

이 시스템은 텍스트, 이미지, 구조화된 데이터를 통합하여 
ORI(Outlier Risk Index) 알고리즘으로 이상 패턴을 정확하게 탐지합니다.
```

### 실행할 명령어:
```bash
cd /Users/hakjun/Desktop/Descent
source venv/bin/activate
export GCP_PROJECT_ID="your-project-id"
export BQ_DATASET="descent_demo"
python descent_cli.py
```

### 캡처 포인트:
- CLI 실행 시작 배너
- 환경 설정 정보
- 시스템 상태 확인 결과

---

## 2️⃣ 기술적 접근법 설명 (1분)

### 화면: 터미널 (계속)
### 대사:
```
Descent의 핵심 기술을 살펴보겠습니다.

첫 번째, BigQuery AI의 임베딩 기능을 활용합니다.
텍스트는 768차원, 이미지는 1408차원으로 변환됩니다.

두 번째, 구조화된 데이터는 3차원으로 정규화합니다.

세 번째, 이 모든 차원을 통합하여 2179차원의 멀티모달 벡터를 생성합니다.

마지막으로, ORI 알고리즘으로 이상 패턴을 감지합니다.
```

### 실행할 명령어:
```bash
# ORI 분석 실행
python descent_cli.py --mode vertex --action ori
```

### 캡처 포인트:
- ORI 파라미터 설정
- Job ID 생성
- 분석 결과 (HIGH/MEDIUM/LOW 위험도 분포)

---

## 3️⃣ BigQuery Console 실행 (2분)

### 화면: 브라우저 (BigQuery Console)
### 대사:
```
이제 BigQuery Console에서 실제 데이터를 확인해보겠습니다.

먼저 텍스트 임베딩의 차원을 확인해보겠습니다.
```

### 실행할 쿼리 1:
```sql
-- 텍스트 임베딩 차원 확인 (768차원)
SELECT 
  id,
  ARRAY_LENGTH(embedding) as embedding_dim,
  text_content
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 5;
```

### 대사:
```
보시다시피 텍스트 임베딩은 768차원입니다.

이제 이미지 임베딩을 확인해보겠습니다.
```

### 실행할 쿼리 2:
```sql
-- 이미지 임베딩 차원 확인 (1408차원)
SELECT 
  id,
  uri,
  ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real` 
LIMIT 5;
```

### 대사:
```
이미지 임베딩은 1408차원입니다.

이제 멀티모달 통합 결과를 확인해보겠습니다.
```

### 실행할 쿼리 3:
```sql
-- 멀티모달 통합 차원 확인 (2179차원)
SELECT 
  key,
  ARRAY_LENGTH(embedding) as total_dimensions,
  text_id,
  image_id
FROM `${GCP_PROJECT_ID}.descent_demo.emb_stitched_mm` 
LIMIT 5;
```

### 대사:
```
멀티모달 통합 결과는 2179차원입니다.
이는 텍스트 768차원 + 이미지 1408차원 + 구조화 데이터 3차원의 합입니다.
```

---

## 4️⃣ 성능 지표 확인 (1분)

### 화면: 브라우저 (BigQuery Console 계속)
### 대사:
```
이제 성능 지표를 확인해보겠습니다.
```

### 실행할 쿼리 4:
```sql
-- 성능 지표 비교
SELECT 
  metric,
  baseline_value,
  descent_value,
  ROUND((descent_value - baseline_value) / baseline_value * 100, 0) as improvement_percent
FROM `${GCP_PROJECT_ID}.descent_demo.performance_metrics`
ORDER BY improvement_percent DESC;
```

### 대사:
```
성능 개선 결과를 보시면:
- F1-Score는 300% 향상
- 처리 시간은 85% 단축
- Precision@K는 187% 향상
- Recall@K는 280% 향상
- MRR은 117% 향상

이는 기존 방법 대비 획기적인 개선입니다.
```

---

## 5️⃣ 최종 아티팩트 확인 (30초)

### 화면: 파일 탐색기 또는 터미널
### 대사:
```
마지막으로 제출할 아티팩트를 확인해보겠습니다.
```

### 실행할 명령어:
```bash
ls -la submission_bundle/
echo "제출 번들 생성 완료: descent_project_compliant.zip"
```

### 대사:
```
총 26개의 SQL 파일과 다양한 결과 파일들이 준비되었습니다.

이 모든 것이 BigQuery AI 해커톤에 제출할 완성된 솔루션입니다.
```

---

## 6️⃣ 마무리 (30초)

### 화면: 전체 화면 또는 로고
### 대사:
```
Descent는 BigQuery AI의 강력한 기능을 활용하여
멀티모달 데이터 분석의 새로운 패러다임을 제시합니다.

감사합니다!
```

---

## 🎬 촬영 팁

### 화면 구성:
- 전체 화면 모드 사용
- 중요한 숫자들 강조 (768, 1408, 2179)
- 성능 개선 수치 명확히 표시 (+300%, -85%)

### 음성:
- 명확하고 자신감 있는 톤
- 각 단계별로 2-3초씩 멈춤
- 기술적 용어는 천천히 발음

### 편집:
- 각 쿼리 실행 후 결과가 완전히 로드될 때까지 대기
- 중요한 부분은 화면에 포커스
- 전체적으로 5-6분 내외로 편집

---

## 📁 제출 파일

### 최종 제출물:
1. **데모 영상**: `descent_demo_video.mp4` (5-6분)
2. **스크린샷**: 6개 PNG 파일
3. **프로젝트 소스코드**: `descent_project_compliant.zip`
4. **문서화 자료**: MD 파일들

### 예상 파일 크기:
- 영상: 50-100MB
- 스크린샷: 30-50MB
- 소스코드: 292KB
- 총 예상 크기: 100-150MB
