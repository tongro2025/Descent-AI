# 🎬 CLI 실행 녹화 스크립트

## 📋 녹화 순서 및 대사

### 1️⃣ 인트로 (10초)
**대사:**
```
안녕하세요! BigQuery AI 해커톤에 참여한 Descent 팀입니다.

오늘은 멀티모달 데이터의 불일치를 감지하는 혁신적인 시스템을 소개하겠습니다.
```

### 2️⃣ 프로젝트 설정 (30초)
**대사:**
```
먼저 프로젝트 디렉토리로 이동하고 환경을 설정하겠습니다.
```

**실행할 명령어:**
```bash
cd /Users/hakjun/Desktop/Descent
pwd
ls -la
```

### 3️⃣ 가상환경 활성화 (20초)
**대사:**
```
Python 가상환경을 활성화하겠습니다.
```

**실행할 명령어:**
```bash
source venv/bin/activate
which python
python --version
```

### 4️⃣ 환경변수 설정 (20초)
**대사:**
```
BigQuery 연결을 위한 환경변수를 설정하겠습니다.
```

**실행할 명령어:**
```bash
export GCP_PROJECT_ID="your-project-id"
export BQ_DATASET="descent_demo"
echo "GCP_PROJECT_ID: $GCP_PROJECT_ID"
echo "BQ_DATASET: $BQ_DATASET"
```

### 5️⃣ CLI 실행 (1분)
**대사:**
```
이제 Descent CLI를 실행하겠습니다.
```

**실행할 명령어:**
```bash
python descent_cli.py
```

**예상 출력:**
```
🎬 ==========================================
🚀 Multimodal Descent: ORI-based Discrepancy Detection
📊 BigQuery AI Hackathon 2024 - Championship Level
🎬 ==========================================

📋 Environment Configuration:
  GCP_PROJECT_ID: your-project-id
  BQ_DATASET: descent_demo
  MODE: vertex
  LOCATION: US

📊 System Status Check
📊 ==========================================
📊 시스템 상태 확인
프로젝트: your-project-id
데이터셋: descent_demo
모드: vertex
위치: US
아티팩트 파일 수: 32

BigQuery 연결: ✅ (0개 데이터셋)
```

### 6️⃣ ORI 분석 실행 (1분)
**대사:**
```
이제 ORI 분석을 실행하겠습니다.
```

**실행할 명령어:**
```bash
python descent_cli.py --mode vertex --action ori
```

**예상 출력:**
```
🎯 ==========================================
🎯 ORI Analysis Execution
🎯 ==========================================

ORI 파라미터 설정:
  - Weight: 0.7
  - Threshold: 0.3
  - Mode: vertex

실행 중...
Job ID: 49f5f335-9c4c-4946-b4e5-3cb71dc2d3af
Status: RUNNING

✅ ORI 분석 완료!
📊 분석 결과:
  - 총 처리된 레코드: 1,000개
  - HIGH 위험도: 15개 (1.5%)
  - MEDIUM 위험도: 85개 (8.5%)
  - LOW 위험도: 900개 (90.0%)

🎉 ORI 분석이 성공적으로 완료되었습니다!
```

### 7️⃣ 마무리 (10초)
**대사:**
```
CLI 실행이 성공적으로 완료되었습니다.
다음 단계로 BigQuery Console에서 실제 데이터를 확인해보겠습니다.
```

## 🎥 녹화 팁

### 화면 구성:
- 전체 터미널 화면을 보여주세요
- 명령어 입력과 출력을 명확히 구분
- 중요한 메시지가 나타날 때 잠시 멈춤

### 음성:
- 명확하고 자신감 있는 톤
- 각 단계별로 설명
- 기술적 용어는 천천히 발음

### 편집:
- 각 명령어 실행 후 결과가 완전히 표시될 때까지 대기
- 중요한 부분은 화면에 포커스
- 전체적으로 2-3분 내외로 편집

## 📁 예상 결과

### 녹화 파일:
- `cli_execution_demo.mp4` (2-3분)

### 핵심 장면:
1. CLI 실행 시작 배너
2. 환경 설정 과정
3. BigQuery 연결 상태 확인
4. ORI 분석 실행 및 완료
5. 분석 결과 표시

## ⚠️ 주의사항

### 실제 실행 시:
- BigQuery 접근 권한이 필요합니다
- 현재 `your-project-id`는 플레이스홀더입니다
- 실제 프로젝트 ID로 변경 필요

### 녹화 시:
- 화면 녹화 소프트웨어를 먼저 실행하세요
- 터미널 창을 전체 화면으로 설정하세요
- 중요한 메시지가 나타날 때 잠시 멈춤
