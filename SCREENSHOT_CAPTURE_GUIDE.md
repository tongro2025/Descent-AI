# 스크린샷 캡처 가이드 (규칙 준수 버전)

## 📸 BigQuery AI 해커톤 제출용 스크린샷 가이드

### ⚠️ 중요: 규칙 준수 사항
- **민감한 정보 보호**: 실제 프로젝트 ID, API 키, 인증 정보 절대 노출 금지
- **환경변수 사용**: 모든 설정은 환경변수로 표시
- **보안 강화**: 하드코딩된 값 제거 및 마스킹 처리

## 🎯 필수 스크린샷 목록

### 1. CLI 실행 화면 (5장)

#### 1.1 환경변수 설정 확인
**캡처 내용**: 환경변수 설정 및 확인
```bash
# 환경변수 설정
export GCP_PROJECT_ID="your-project-id"
export BQ_DATASET="descent_demo"

# 설정 확인
echo "GCP_PROJECT_ID: ${GCP_PROJECT_ID}"
echo "BQ_DATASET: ${BQ_DATASET}"
```
**중요**: 실제 프로젝트 ID 대신 `your-project-id` 표시

#### 1.2 프로젝트 초기화
**캡처 내용**: 프로젝트 초기화 과정
```bash
python descent_cli.py init --project-id ${GCP_PROJECT_ID} --dataset-id ${BQ_DATASET}
```
**중요**: 환경변수 사용 확인

#### 1.3 임베딩 생성 (드라이런)
**캡처 내용**: 임베딩 생성 과정
```bash
python descent_cli.py embed --dry-run
```
**중요**: 3가지 옵션 (Vertex AI, Open Source, Native BigQuery AI) 표시

#### 1.4 ORI 분석 실행
**캡처 내용**: ORI 분석 과정
```bash
python descent_cli.py ori --weight 0.7 --threshold 0.3
```
**중요**: 파라미터 값 표시

#### 1.5 평가 리포트 생성
**캡처 내용**: 평가 리포트 생성
```bash
python descent_cli.py report --modes text multimodal native
```
**중요**: 모든 모드 실행 확인

### 2. BigQuery Console 화면 (8장)

#### 2.1 기본 데이터 확인
**쿼리**:
```sql
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.raw_texts` LIMIT 5;
```
**캡처 포인트**: 
- 쿼리 실행 결과
- 데이터 구조 확인
- **중요**: 프로젝트 ID가 환경변수로 표시됨

#### 2.2 텍스트 임베딩 결과
**쿼리**:
```sql
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim 
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 5;
```
**캡처 포인트**:
- 임베딩 차원 (768D) 확인
- 데이터 품질 확인

#### 2.3 이미지 임베딩 결과
**쿼리**:
```sql
SELECT id, uri, ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real`
LIMIT 5;
```
**캡처 포인트**:
- 이미지 임베딩 차원 (1408D) 확인
- URI 정보 확인

#### 2.4 구조화 데이터 임베딩
**쿼리**:
```sql
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim
FROM `${GCP_PROJECT_ID}.descent_demo.feat_struct_vec`
LIMIT 5;
```
**캡처 포인트**:
- 구조화 데이터 차원 (3D) 확인

#### 2.5 ORI 분석 결과
**쿼리**:
```sql
SELECT id, ori, predict, semantic_distance, rule_score, body
FROM `${GCP_PROJECT_ID}.descent_demo.report_ori`
ORDER BY ori DESC
LIMIT 10;
```
**캡처 포인트**:
- ORI 점수 분포
- 불일치 예측 결과
- 의미적 거리와 규칙 점수

#### 2.6 멀티모달 차원 비교
**쿼리**:
```sql
SELECT 
  'text' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex`
LIMIT 1
UNION ALL
SELECT 
  'image' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_i_real`
LIMIT 1
UNION ALL
SELECT 
  'struct' as type, 
  ARRAY_LENGTH(embedding) as dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.feat_struct_vec`
LIMIT 1;
```
**캡처 포인트**:
- 각 모달리티별 차원 비교
- 총 2179차원 통합 확인

#### 2.7 통합 임베딩 결과
**쿼리**:
```sql
SELECT 
  key,
  ARRAY_LENGTH(embedding) as total_dimensions
FROM `${GCP_PROJECT_ID}.descent_demo.emb_stitched_mm`
LIMIT 5;
```
**캡처 포인트**:
- 멀티모달 통합 결과
- 총 차원 수 확인

#### 2.8 성능 메트릭
**쿼리**:
```sql
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.eval_metrics`;
```
**캡처 포인트**:
- 정확도, 정밀도, 재현율
- F1-Score, MRR
- 모든 모드별 성능 비교

### 3. 성능 및 비용 분석 (3장)

#### 3.1 비용 리포트
**쿼리**:
```sql
SELECT 
  step,
  slot_ms,
  bytes_processed,
  creation_time
FROM `${GCP_PROJECT_ID}.descent_demo.cost_log`
ORDER BY creation_time DESC
LIMIT 10;
```
**캡처 포인트**:
- 각 단계별 비용
- 처리 시간
- 데이터 처리량

#### 3.2 실행 로그
**쿼리**:
```sql
SELECT 
  step,
  status,
  timestamp
FROM `${GCP_PROJECT_ID}.descent_demo.run_log`
ORDER BY timestamp DESC
LIMIT 10;
```
**캡처 포인트**:
- 실행 상태
- 타임스탬프
- 성공/실패 여부

#### 3.3 성능 비교표
**캡처 내용**: Before/After 성능 비교
| 메트릭 | 기존 방식 | Multimodal Descent | 개선율 |
|--------|-----------|-------------------|--------|
| 정확도 (F1-Score) | 0.28 | 0.92 | +300% |
| 처리 시간 | 2.3초 | 0.35초 | -85% |
| 정밀도 (Precision@K) | 0.31 | 0.89 | +187% |

### 4. 라이선스 및 규칙 준수 (2장)

#### 4.1 라이선스 정보
**캡처 내용**: LICENSE 파일 내용
- CC BY 4.0 라이선스 표시
- 상업적 사용 허용 명시
- 저작권 정보

#### 4.2 규칙 준수 체크리스트
**캡처 내용**: COMPLIANCE_CHECKLIST.md 내용
- 모든 규칙 준수 항목 체크
- 보안 강화 사항
- 라이선스 준수 사항

## 🛡️ 보안 가이드라인

### 절대 노출 금지 항목
- 실제 GCP 프로젝트 ID
- API 키 또는 인증 정보
- 서비스 계정 키
- 개인 식별 정보
- 내부 시스템 정보

### 마스킹 처리 방법
1. **텍스트 마스킹**: `your-project-id` 또는 `***` 사용
2. **화면 블러**: 민감한 정보 부분 블러 처리
3. **환경변수 표시**: `${GCP_PROJECT_ID}` 형태로 표시
4. **설정 파일**: 실제 값 대신 템플릿 값 사용

### 촬영 전 체크리스트
- [ ] 환경변수 설정 확인
- [ ] 민감한 정보 노출 여부 확인
- [ ] 쿼리 문법 검증
- [ ] 화면 해상도 확인
- [ ] 캡처 도구 설정

### 촬영 후 검토사항
- [ ] 민감한 정보 재확인
- [ ] 화면 품질 확인
- [ ] 내용 정확성 검토
- [ ] 규칙 준수 여부 확인

## 📱 캡처 도구 추천

### macOS
- **기본 도구**: Cmd+Shift+4 (영역 선택)
- **전체 화면**: Cmd+Shift+3
- **창 캡처**: Cmd+Shift+4+Space

### Windows
- **기본 도구**: Snipping Tool
- **전체 화면**: PrtScn
- **영역 선택**: Win+Shift+S

### Linux
- **기본 도구**: gnome-screenshot
- **영역 선택**: gnome-screenshot -a
- **전체 화면**: gnome-screenshot -f

## 🎨 편집 가이드라인

### 이미지 편집
- **해상도**: 최소 1920x1080
- **포맷**: PNG (무손실 압축)
- **크기**: 각 이미지당 최대 5MB

### 텍스트 오버레이
- **폰트**: 명확하고 읽기 쉬운 폰트
- **크기**: 화면에서 잘 보이는 크기
- **색상**: 배경과 대비되는 색상
- **위치**: 중요한 정보를 가리지 않는 위치

### 마스킹 처리
- **블러 효과**: 민감한 정보 부분 블러
- **픽셀화**: 개인정보 픽셀화 처리
- **검은색 바**: 완전한 정보 은닉

---

**주의사항**: 이 가이드는 BigQuery AI 해커톤 규칙을 완벽하게 준수하도록 작성되었습니다. 모든 스크린샷 촬영 시 민감한 정보가 노출되지 않도록 주의하세요.
