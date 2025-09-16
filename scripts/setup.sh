#!/usr/bin/env bash
set -euo pipefail

# env
if [ -f .env ]; then export $(grep -v '^#' .env | xargs); fi

bq --location="${BQ_LOCATION}" mk -d -f "${GCP_PROJECT}:${BQ_DATASET}" || true

echo "[OK] BigQuery dataset '${BQ_DATASET}' ready in ${BQ_LOCATION}"
echo "다음 쿼리를 실행해 샘플 테이블을 만듭니다: sql/01_schema.sql"

