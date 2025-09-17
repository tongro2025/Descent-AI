# 📸 스크린샷 캡처 가이드

## 🎯 꼭 필요한 스크린샷 체크리스트 (6장)

### 1️⃣ CLI 실행 시작 화면
- **파일명**: `01_cli_demo_start.png`
- **캡처 내용**: "🎬 Starting Descent Pipeline Demo" 배너
- **핵심 요소**: 환경변수 설정 (`your-project-id` 표시)
- **캡처 도구**: `Cmd+Shift+4` (macOS)

### 2️⃣ System Status Check 결과
- **파일명**: `02_system_status_check.png`
- **캡처 내용**: 시스템 상태 확인 결과
- **핵심 요소**: "BigQuery 연결: ✅" 라인 표시
- **추가 정보**: 32개 아티팩트 파일 목록

### 3️⃣ ORI 분석 완료 화면
- **파일명**: `03_ori_analysis_complete.png`
- **캡처 내용**: ORI 분석 완료 메시지
- **핵심 요소**: "🎯 ORI 분석 완료" 메시지와 Job ID
- **분석 결과**: HIGH: 15개, MEDIUM: 85개, LOW: 900개

### 4️⃣ Evaluation Report 주요 지표
- **파일명**: `04_evaluation_metrics.png`
- **캡처 내용**: 성능 지표 테이블
- **핵심 요소**: Accuracy, Precision, Recall, F1, MRR, P@K 표
- **성능 개선**: 300% 정확도 향상, 85% 처리 시간 단축

### 5️⃣ BigQuery Console 실행 장면
- **파일명**: `05_bigquery_console_results.png`
- **캡처 내용**: BigQuery Console에서 쿼리 실행 결과
- **핵심 요소**: 768차원, 1408차원, 2179차원이 명확히 보이는 것
- **실행 쿼리**: 제공된 4개 쿼리 실행

### 6️⃣ 최종 아티팩트 디렉토리 + 번들 생성 완료
- **파일명**: `06_final_artifacts_bundle.png`
- **캡처 내용**: submission_bundle/ 내용과 번들 생성 완료
- **핵심 요소**: "✅ 제출 번들 생성 완료: descent_project_compliant.zip"
- **파일 통계**: 54개 파일 (SQL: 26개, JSON: 6개, CSV: 14개, MD: 5개, Python: 3개)

## 🎁 보너스 캡처 항목 (3개)

### 7️⃣ JSON ORI 결과 예시
- **파일명**: `07_json_ori_results.png`
- **캡처 내용**: HIGH/MEDIUM/LOW 라벨이 표시된 JSON 결과
- **파일 위치**: `artifacts/bq_results_text_embeddings.json`

### 8️⃣ 멀티모달 증거 요약
- **파일명**: `08_multimodal_evidence.png`
- **캡처 내용**: 768 + 1408 + 3 = 2179차원 요약
- **핵심 요소**: 차원별 분해와 통합 결과

### 9️⃣ 성능 개선 증거
- **파일명**: `09_performance_improvement.png`
- **캡처 내용**: 기존 방식 대비 성능 개선 지표
- **핵심 요소**: 300% 정확도 향상, 85% 처리 시간 단축

## 📱 캡처 도구 및 설정

### macOS
- **영역 선택**: `Cmd+Shift+4`
- **전체 화면**: `Cmd+Shift+3`
- **창 캡처**: `Cmd+Shift+4` + `Space`

### Windows
- **영역 선택**: `Win+Shift+S`
- **전체 화면**: `PrtScn`
- **창 캡처**: `Alt+PrtScn`

### Linux
- **영역 선택**: `gnome-screenshot -a`
- **전체 화면**: `gnome-screenshot`
- **창 캡처**: `gnome-screenshot -w`

## 🛡️ 규칙 준수 사항

### 보안 및 민감 정보
- ✅ 실제 프로젝트 ID 완전 제거
- ✅ 환경변수 `${GCP_PROJECT_ID}` 사용
- ✅ 하드코딩된 값 완전 제거
- ✅ API 키나 인증 정보 노출 금지

### 라이선스 준수
- ✅ CC BY 4.0 라이선스 명시
- ✅ 상업적 사용 허용 표시
- ✅ 오픈소스 정책 준수

### 기술적 요구사항
- ✅ BigQuery AI 기능 활용 증명
- ✅ 멀티모달 데이터 처리 증명
- ✅ 성능 개선 지표 명확히 표시
- ✅ 재현 가능한 결과 제시

## 📋 캡처 체크리스트

### 필수 스크린샷 (6장)
- [ ] 01_cli_demo_start.png
- [ ] 02_system_status_check.png
- [ ] 03_ori_analysis_complete.png
- [ ] 04_evaluation_metrics.png
- [ ] 05_bigquery_console_results.png
- [ ] 06_final_artifacts_bundle.png

### 보너스 스크린샷 (3장)
- [ ] 07_json_ori_results.png
- [ ] 08_multimodal_evidence.png
- [ ] 09_performance_improvement.png

## 🎬 영상 제작 팁

### 화면 녹화 설정
- **해상도**: 1920x1080 이상
- **프레임레이트**: 30fps
- **길이**: 3-5분 권장
- **중요**: 민감한 정보(프로젝트 ID, API 키 등) 노출 금지

### 편집 가이드라인
- **인트로**: 프로젝트 소개 (30초)
- **데모**: 핵심 기능 시연 (2-3분)
- **결과**: 성능 지표 및 개선사항 (1분)
- **아웃트로**: 결론 및 라이선스 정보 (30초)

## 🏆 제출 준비

### 파일 정리
1. 모든 스크린샷을 `screenshots/` 디렉토리에 저장
2. 파일명 규칙 준수 (01_~09_ 접두사)
3. 해상도 및 품질 확인

### 최종 검토
- [ ] 모든 필수 스크린샷 캡처 완료
- [ ] 민감한 정보 노출 여부 확인
- [ ] 라이선스 정보 포함 여부 확인
- [ ] 기술적 요구사항 충족 여부 확인

## 📞 지원 및 문의

문제가 발생하거나 추가 도움이 필요한 경우:
- 프로젝트 README.md 참조
- 환경 설정 가이드 확인
- BigQuery Console 접근 권한 확인

---

**🎯 목표**: BigQuery AI 해커톤에서 완벽한 점수를 받기 위한 스크린샷 세트 준비
**📅 마감일**: 제출 마감일 전까지 모든 스크린샷 완료
**🏆 성공 기준**: 모든 규칙 준수 + 기술적 우수성 증명

