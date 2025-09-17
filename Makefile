# Descent Pipeline Makefile - Championship Level
# P3: Code·CI/CD·Readability

.PHONY: help init embed stitch ori report test clean status install deps

# Default settings
CONFIG_FILE ?= config.yaml
PROJECT_ID ?= your-project-id
DATASET_ID ?= descent_demo
MODE ?= vertex

# Help
help:
	@echo "Descent Pipeline - Championship Level Makefile"
	@echo "=============================================="
	@echo ""
	@echo "Basic commands:"
	@echo "  make init          - Initialize project"
	@echo "  make embed         - Generate embeddings"
	@echo "  make stitch        - Multimodal stitching"
	@echo "  make ori           - ORI analysis"
	@echo "  make report        - Generate evaluation report"
	@echo "  make test          - Integration tests"
	@echo "  make clean         - Cleanup"
	@echo "  make status        - System status check"
	@echo ""
	@echo "Development tools:"
	@echo "  make install       - Install dependencies"
	@echo "  make deps          - Check dependencies"
	@echo "  make lint          - Code linting"
	@echo "  make format        - Code formatting"
	@echo ""
	@echo "CI/CD:"
	@echo "  make ci-test       - CI tests"
	@echo "  make ci-report     - CI reports"
	@echo "  make bundle        - Create submission bundle"
	@echo ""
	@echo "Settings:"
	@echo "  CONFIG_FILE=config.yaml  - Configuration file"
	@echo "  PROJECT_ID=your-project  - GCP project"
	@echo "  DATASET_ID=descent_demo  - BigQuery dataset"
	@echo "  MODE=vertex              - Execution mode"

# 프로젝트 초기화
init:
	@echo "🚀 프로젝트 초기화"
	python3 descent_cli.py init --project-id $(PROJECT_ID) --dataset-id $(DATASET_ID) --mode $(MODE) --config-file $(CONFIG_FILE)

# 임베딩 생성
embed:
	@echo "🧠 임베딩 생성"
	python3 descent_cli.py embed --config-file $(CONFIG_FILE)

# 멀티모달 스티칭
stitch:
	@echo "🔗 멀티모달 스티칭"
	python3 descent_cli.py stitch --config-file $(CONFIG_FILE)

# ORI 분석
ori:
	@echo "🎯 ORI 분석"
	python3 descent_cli.py ori --config-file $(CONFIG_FILE)

# 평가 리포트 생성
report:
	@echo "📊 평가 리포트 생성"
	python3 descent_cli.py report --config-file $(CONFIG_FILE)

# 통합 테스트
test:
	@echo "🧪 통합 테스트"
	python3 descent_cli.py test --config-file $(CONFIG_FILE)

# 정리 작업
clean:
	@echo "🧹 정리 작업"
	python3 descent_cli.py clean --config-file $(CONFIG_FILE)

# 시스템 상태 확인
status:
	@echo "📊 시스템 상태 확인"
	python3 descent_cli.py status --config-file $(CONFIG_FILE)

# 의존성 설치
install:
	@echo "📦 의존성 설치"
	pip install -r requirements.txt
	pip install typer pyyaml pandas scikit-learn

# 의존성 확인
deps:
	@echo "🔍 의존성 확인"
	pip check

# 코드 린팅
lint:
	@echo "🔍 코드 린팅"
	ruff check .
	mypy descent_pipeline_v2.py eval_harness.py descent_cli.py

# 코드 포맷팅
format:
	@echo "🎨 코드 포맷팅"
	black .
	ruff check --fix .

# CI 테스트
ci-test:
	@echo "🤖 CI 테스트"
	python3 descent_cli.py test --test-mode mini --config-file $(CONFIG_FILE)

# CI 리포트
ci-report:
	@echo "📊 CI 리포트"
	python3 descent_cli.py report --config-file $(CONFIG_FILE) --output-format json

# 제출 번들 생성
bundle:
	@echo "📦 제출 번들 생성"
	mkdir -p submission_bundle
	cp -r artifacts/ submission_bundle/
	cp -r sql/ submission_bundle/
	cp *.py submission_bundle/
	cp *.yaml submission_bundle/
	cp *.md submission_bundle/
	cp Makefile submission_bundle/
	cp requirements.txt submission_bundle/
	cd submission_bundle && zip -r ../descent_submission.zip .
	@echo "✅ 제출 번들 생성 완료: descent_submission.zip"

# 전체 파이프라인 실행
pipeline: init embed stitch ori report
	@echo "🎉 전체 파이프라인 완료"

# 빠른 테스트 (OSS 모드)
quick-test:
	@echo "⚡ 빠른 테스트 (OSS 모드)"
	python3 descent_cli.py test --test-mode mini --config-file $(CONFIG_FILE)

# 성능 벤치마크
benchmark:
	@echo "⚡ 성능 벤치마크"
	time python3 descent_cli.py embed --config-file $(CONFIG_FILE)
	time python3 descent_cli.py ori --config-file $(CONFIG_FILE)
	time python3 descent_cli.py report --config-file $(CONFIG_FILE)

# 보안 스캔
security-scan:
	@echo "🔒 보안 스캔"
	pip install safety
	safety check
	@echo "✅ 보안 스캔 완료"

# 문서 생성
docs:
	@echo "📚 문서 생성"
	python3 descent_cli.py report --config-file $(CONFIG_FILE) --output-format markdown > README_EVALUATION.md
	@echo "✅ 문서 생성 완료"

# 백업
backup:
	@echo "💾 백업 생성"
	tar -czf descent_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz artifacts/ sql/ *.py *.yaml *.md Makefile requirements.txt
	@echo "✅ 백업 생성 완료"

# 복원
restore:
	@echo "🔄 복원"
	@echo "사용법: make restore BACKUP_FILE=backup_file.tar.gz"
	@if [ -z "$(BACKUP_FILE)" ]; then echo "❌ BACKUP_FILE이 지정되지 않았습니다"; exit 1; fi
	tar -xzf $(BACKUP_FILE)
	@echo "✅ 복원 완료"

# 모니터링
monitor:
	@echo "📊 모니터링"
	@echo "프로젝트: $(PROJECT_ID)"
	@echo "데이터셋: $(DATASET_ID)"
	@echo "모드: $(MODE)"
	@echo "설정 파일: $(CONFIG_FILE)"
	@echo ""
	@echo "아티팩트 상태:"
	@ls -la artifacts/ 2>/dev/null || echo "아티팩트 없음"
	@echo ""
	@echo "로그 상태:"
	@ls -la logs/ 2>/dev/null || echo "로그 없음"

# 개발 모드
dev: install lint format test
	@echo "🔧 개발 환경 설정 완료"

# 프로덕션 모드
prod: clean install pipeline
	@echo "🚀 프로덕션 배포 완료"

# 기본 타겟
.DEFAULT_GOAL := help