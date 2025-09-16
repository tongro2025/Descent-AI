import os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT = os.getenv("GCP_PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_LOCATION = os.getenv("BQ_LOCATION", "US")

# 임베딩 모델 설정
USE_REAL_EMBEDDINGS = os.getenv("USE_REAL_EMBEDDINGS", "true").lower() == "true"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models.text_embedding")
USE_MULTIMODAL = os.getenv("USE_MULTIMODAL", "false").lower() == "true"

# ORI 알고리즘 파라미터
ORI_WEIGHT = float(os.getenv("ORI_WEIGHT", "0.7"))
ORI_THRESHOLD = float(os.getenv("ORI_THRESHOLD", "0.3"))

def fq(table: str) -> str:
    return f"{GCP_PROJECT}.{BQ_DATASET}.{table}"

