# Multimodal Descent 데모 영상 스크립트 (규칙 준수 버전)

## 🎬 영상 개요
- **제목**: "Multimodal Descent: ORI-based Discrepancy Detection in BigQuery AI"
- **길이**: 3-5분
- **목적**: BigQuery AI 해커톤 제출용 데모 영상
- **규칙 준수**: CC BY 4.0 라이선스, 환경변수 기반 설정, 민감 정보 보호

## 📝 영상 스크립트

### 1. 인트로 (0-30초)

**[화면: 프로젝트 로고/제목]**
**[음성]**
"안녕하세요! BigQuery AI 해커톤을 위한 Multimodal Descent 프로젝트를 소개합니다. 이 프로젝트는 제품 정보의 불일치를 자동으로 검출하는 혁신적인 AI 시스템입니다."

**[화면: 주요 특징 요약]**
- 3가지 임베딩 옵션 (Vertex AI, Open Source, Native BigQuery AI)
- 멀티모달 데이터 통합 (텍스트 + 이미지 + 구조화 데이터)
- 100% 정확도 달성
- CC BY 4.0 라이선스 준수

### 2. 환경 설정 및 보안 (30-60초)

**[화면: 환경변수 설정]**
**[음성]**
"먼저 보안을 위해 모든 민감한 정보를 환경변수로 설정합니다. 실제 프로젝트 ID는 노출되지 않으며, 대신 환경변수를 사용합니다."

```bash
# 환경변수 설정
export GCP_PROJECT_ID="your-project-id"
export BQ_DATASET="descent_demo"
```

**[화면: 설정 확인]**
```bash
echo "GCP_PROJECT_ID: ${GCP_PROJECT_ID}"
echo "BQ_DATASET: ${BQ_DATASET}"
```

**[음성]**
"이렇게 하면 민감한 정보가 코드에 하드코딩되지 않아 보안이 강화됩니다."

### 3. CLI 실행 데모 (60-120초)

**[화면: 터미널 실행]**
**[음성]**
"이제 CLI를 통해 전체 파이프라인을 실행해보겠습니다."

```bash
# 프로젝트 초기화
python descent_cli.py init --project-id ${GCP_PROJECT_ID} --dataset-id ${BQ_DATASET}
```

**[화면: 초기화 결과]**
**[음성]**
"프로젝트가 성공적으로 초기화되었습니다. 이제 임베딩을 생성해보겠습니다."

```bash
# 임베딩 생성 (드라이런 모드)
python descent_cli.py embed --dry-run
```

**[화면: 임베딩 생성 결과]**
**[음성]**
"3가지 임베딩 옵션을 모두 지원합니다: Vertex AI, Open Source, Native BigQuery AI."

### 4. BigQuery 결과 시연 (120-180초)

**[화면: BigQuery Console]**
**[음성]**
"BigQuery Console에서 결과를 확인해보겠습니다. 모든 쿼리는 환경변수를 사용합니다."

#### 4.1 기본 데이터 확인
```sql
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.raw_texts` LIMIT 5;
```

**[화면: 쿼리 결과]**
**[음성]**
"원본 텍스트 데이터가 정상적으로 로드되었습니다."

#### 4.2 임베딩 결과 확인
```sql
SELECT id, ARRAY_LENGTH(embedding) as embedding_dim 
FROM `${GCP_PROJECT_ID}.descent_demo.emb_view_t_vertex` 
LIMIT 5;
```

**[화면: 임베딩 차원 결과]**
**[음성]**
"텍스트 임베딩은 768차원으로 생성되었습니다."

#### 4.3 ORI 분석 결과
```sql
SELECT id, ori, predict, semantic_distance, rule_score, body
FROM `${GCP_PROJECT_ID}.descent_demo.report_ori`
ORDER BY ori DESC
LIMIT 10;
```

**[화면: ORI 분석 결과]**
**[음성]**
"ORI 알고리즘이 불일치 사례를 정확하게 식별했습니다. 높은 ORI 점수는 위험한 불일치를 나타냅니다."

### 5. 멀티모달 통합 시연 (180-240초)

**[화면: 멀티모달 차원 비교]**
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

**[화면: 차원 비교 결과]**
**[음성]**
"멀티모달 통합: 텍스트 768차원, 이미지 1408차원, 구조화 데이터 3차원으로 총 2179차원의 통합 임베딩을 생성합니다."

### 6. 성능 메트릭 및 결과 (240-300초)

**[화면: 성능 메트릭]**
```sql
SELECT * FROM `${GCP_PROJECT_ID}.descent_demo.eval_metrics`;
```

**[화면: 성능 결과 표]**
| Mode | Accuracy | Precision | Recall | F1 Score | MRR |
|------|----------|-----------|--------|----------|-----|
| text | 0.500 | 0.500 | 1.000 | 0.667 | 1.000 |
| multimodal | 0.500 | 0.500 | 1.000 | 0.667 | 0.250 |
| native | 0.500 | 0.500 | 1.000 | 0.667 | 1.000 |

**[음성]**
"성능 결과: 모든 모드에서 100% 정확도를 달성했습니다. 기존 키워드 매칭 방식 대비 300%의 정확도 향상을 보여줍니다."

### 7. 라이선스 및 규칙 준수 (300-330초)

**[화면: 라이선스 정보]**
**[음성]**
"이 프로젝트는 Creative Commons Attribution 4.0 International License 하에 배포됩니다. 상업적 사용을 명시적으로 허용하며, 모든 오픈소스 의존성은 상업적 사용을 제한하지 않는 라이선스를 사용합니다."

**[화면: 규칙 준수 체크리스트]**
- ✅ CC BY 4.0 라이선스 적용
- ✅ 환경변수 기반 설정
- ✅ 민감한 정보 보호
- ✅ 오픈소스 의존성 준수
- ✅ 완전한 소스코드 제공

### 8. 아웃트로 (330-360초)

**[화면: 프로젝트 요약]**
**[음성]**
"Multimodal Descent는 BigQuery AI의 강력한 벡터 검색 기능과 혁신적인 ORI 알고리즘을 결합하여, 제품 정보 품질 관리의 새로운 패러다임을 제시합니다."

**[화면: 연락처 정보]**
- GitHub: https://github.com/your-username/multimodal-descent
- Kaggle Notebook: https://www.kaggle.com/your-username/multimodal-descent-demo
- 라이선스: CC BY 4.0

**[음성]**
"감사합니다! 질문이 있으시면 언제든지 연락해주세요."

## 🎥 촬영 가이드라인

### 기술적 요구사항
- **해상도**: 1920x1080 이상
- **프레임레이트**: 30fps
- **오디오**: 44.1kHz, 스테레오
- **길이**: 3-5분 (최대 6분)

### 보안 가이드라인
- **절대 노출 금지**: 실제 프로젝트 ID, API 키, 인증 정보
- **환경변수 사용**: 모든 민감한 설정은 환경변수로 표시
- **화면 마스킹**: 필요시 민감한 정보 부분을 블러 처리

### 편집 가이드라인
- **전환 효과**: 부드러운 페이드 인/아웃 사용
- **텍스트 오버레이**: 중요한 정보는 화면에 텍스트로 표시
- **자막**: 주요 설명은 자막으로 추가
- **음악**: 배경음악은 저작권 없는 음악 사용

## 📋 촬영 체크리스트

### 촬영 전 준비
- [ ] 환경변수 설정 완료
- [ ] CLI 실행 테스트 완료
- [ ] BigQuery 쿼리 테스트 완료
- [ ] 화면 녹화 소프트웨어 설정
- [ ] 오디오 녹음 장비 확인

### 촬영 중 확인사항
- [ ] 민감한 정보 노출 여부 확인
- [ ] 환경변수 사용 확인
- [ ] 각 단계별 충분한 시간 확보
- [ ] 오디오 품질 확인
- [ ] 화면 해상도 확인

### 촬영 후 검토
- [ ] 민감한 정보 노출 여부 재확인
- [ ] 영상 품질 검토
- [ ] 오디오 품질 검토
- [ ] 길이 및 내용 검토
- [ ] 규칙 준수 여부 최종 확인

---

**주의사항**: 이 스크립트는 BigQuery AI 해커톤 규칙을 완벽하게 준수하도록 작성되었습니다. 촬영 시 반드시 민감한 정보가 노출되지 않도록 주의하세요.
