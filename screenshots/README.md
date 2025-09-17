# 📸 스크린샷 캡처 실행 스크립트

## 🎯 자동화된 스크린샷 캡처를 위한 실행 스크립트

이 스크립트는 BigQuery AI 해커톤 제출을 위한 필수 스크린샷들을 자동으로 생성합니다.

### 사용법
```bash
# 스크립트 실행 권한 부여
chmod +x capture_screenshots.sh

# 스크린샷 캡처 실행
./capture_screenshots.sh
```

### 생성되는 스크린샷
1. CLI 실행 시작 화면
2. System Status Check 결과
3. ORI 분석 완료 화면
4. Evaluation Report 주요 지표
5. BigQuery Console 실행 장면 (쿼리 제공)
6. 최종 아티팩트 디렉토리 + 번들 생성 완료

### 보너스 항목
7. JSON ORI 결과 예시
8. 멀티모달 증거 요약
9. 성능 개선 증거

### 규칙 준수
- ✅ 민감한 정보 보호 (프로젝트 ID 제거)
- ✅ 환경변수 사용 (`${GCP_PROJECT_ID}`)
- ✅ CC BY 4.0 라이선스 준수
- ✅ 보안 강화 (하드코딩된 값 제거)

### 캡처 도구
- **macOS**: `Cmd+Shift+4`
- **Windows**: `Win+Shift+S`
- **Linux**: `gnome-screenshot -a`

### 파일 저장 위치
- **macOS**: 바탕화면
- **Windows**: 사진 폴더
- **Linux**: 홈 디렉토리

### 품질 기준
- **해상도**: 1920x1080 이상
- **포맷**: PNG
- **압축**: 무손실
- **색상**: 24비트 RGB

### 문제 해결
- 권한 문제: `chmod +x capture_screenshots.sh`
- 환경 문제: 가상환경 활성화 확인
- BigQuery 문제: 인증 정보 확인

### 지원
- 프로젝트 README.md 참조
- 환경 설정 가이드 확인
- 기술 지원팀 문의

---

**🎯 목표**: BigQuery AI 해커톤 제출을 위한 완벽한 스크린샷 세트 자동 생성
**📅 마감일**: 제출 마감일 전까지 모든 스크린샷 완료
**🏆 성공 기준**: 모든 규칙 준수 + 기술적 우수성 증명

