# 📋 환경변수 포함 완전한 iTerm 명령어

## 🎬 데모 영상 녹화용 명령어 순서

### 1️⃣ 프로젝트 디렉토리 이동:
```bash
cd /Users/hakjun/Desktop/Descent
```

### 2️⃣ 현재 위치 확인:
```bash
pwd
```

### 3️⃣ 파일 목록 확인:
```bash
ls -la
```

### 4️⃣ 가상환경 활성화:
```bash
source venv/bin/activate
```

### 5️⃣ Python 버전 확인:
```bash
which python
python --version
```

### 6️⃣ 환경변수 설정 (한 번에):
```bash
export GCP_PROJECT_ID="your-project-id" && export BQ_DATASET="descent_demo" && export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### 7️⃣ 환경변수 확인:
```bash
echo "GCP_PROJECT_ID: $GCP_PROJECT_ID"
echo "BQ_DATASET: $BQ_DATASET"
echo "GOOGLE_CLOUD_PROJECT: $GOOGLE_CLOUD_PROJECT"
```

### 8️⃣ CLI 도움말 확인:
```bash
python descent_cli.py --help
```

### 9️⃣ 시스템 상태 확인:
```bash
python descent_cli.py status
```

### 🔟 ORI 분석 실행:
```bash
python descent_cli.py ori
```

## 🎥 녹화 시 대사

### 인트로 (10초):
```
안녕하세요! BigQuery AI 해커톤에 참여한 Descent 팀입니다.
오늘은 멀티모달 데이터의 불일치를 감지하는 혁신적인 시스템을 소개하겠습니다.
```

### 프로젝트 설정 (30초):
```
먼저 프로젝트 디렉토리로 이동하고 환경을 설정하겠습니다.
```

### 가상환경 활성화 (20초):
```
Python 가상환경을 활성화하겠습니다.
```

### 환경변수 설정 (20초):
```
BigQuery 연결을 위한 환경변수를 설정하겠습니다.
GCP 프로젝트 ID와 데이터셋을 설정합니다.
```

### CLI 실행 (1분):
```
이제 Descent CLI를 실행하겠습니다.
먼저 도움말을 확인해보겠습니다.
```

### 시스템 상태 확인 (30초):
```
시스템 상태를 확인해보겠습니다.
프로젝트 설정과 아티팩트 파일들을 확인할 수 있습니다.
```

### ORI 분석 실행 (1분):
```
이제 ORI 분석을 실행하겠습니다.
이 과정에서 멀티모달 데이터의 이상 패턴을 탐지합니다.
```

### 마무리 (10초):
```
CLI 실행이 완료되었습니다.
다음 단계로 BigQuery Console에서 실제 데이터를 확인해보겠습니다.
```

## ⚠️ 주의사항

### 실제 실행 시:
- BigQuery 접근 권한이 필요합니다
- `your-project-id`는 실제 프로젝트 ID로 변경 필요
- ORI 분석은 실제 BigQuery 권한이 있어야 실행됩니다

### 녹화 시:
- 각 명령어 실행 후 결과가 완전히 표시될 때까지 대기
- 중요한 메시지가 나타날 때 잠시 멈춤
- 전체적으로 3-4분 내외로 녹화

## 📁 예상 결과

### 녹화 파일:
- `cli_execution_demo.mp4` (3-4분)

### 핵심 장면:
1. 프로젝트 설정 과정
2. 환경변수 설정
3. CLI 도움말 표시
4. 시스템 상태 확인
5. ORI 분석 실행 (권한 오류 포함)

## 🔧 환경변수 설명

- `GCP_PROJECT_ID`: Google Cloud 프로젝트 ID
- `BQ_DATASET`: BigQuery 데이터셋 이름
- `GOOGLE_CLOUD_PROJECT`: Google Cloud 프로젝트 ID (중복 설정)

이 환경변수들이 설정되면 BigQuery 연결 시 프로젝트 ID를 자동으로 인식합니다.
