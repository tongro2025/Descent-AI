import argparse
from . import bq
from .config import GCP_PROJECT, BQ_DATASET, USE_REAL_EMBEDDINGS, USE_MULTIMODAL

def step_schema():
    bq.run_sql("sql/01_schema.sql")

def step_sample_data():
    bq.run_sql("sql/05_sample_data.sql")

def step_embed():
    """임베딩 생성 - 실제 모델 또는 더미 벡터"""
    if USE_REAL_EMBEDDINGS:
        print("🤖 실제 BigQuery AI 모델 사용")
        if USE_MULTIMODAL:
            print("🖼️ 멀티모달 임베딩 생성")
            bq.run_sql("sql/02_embeddings_multimodal.sql")
        else:
            print("📝 텍스트 임베딩만 생성")
            bq.run_sql("sql/02_embeddings.sql")
    else:
        print("🎭 더미 벡터 사용")
        bq.run_sql("sql/02_embeddings_dummy.sql")

def step_index():
    bq.run_sql("sql/03_index.sql")

def step_ori_optimization():
    """ORI 최적화 계산 (w=0.7, τ=0.3)"""
    bq.run_sql("sql/12_ori_optimization.sql")

def step_search(query: str = "불일치 사례", top_k: int = 10):
    bq.run_sql("sql/04_search_demo.sql", {"query": query, "top_k": top_k})

def step_compare():
    bq.run_sql("sql/06_before_after.sql")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["schema","sample_data","embed","index","search","compare","ori"])
    ap.add_argument("--query", default="스펙과 이미지의 불일치 사례")
    ap.add_argument("--top_k", type=int, default=10)
    args = ap.parse_args()

    if args.cmd == "schema":
        step_schema()
    elif args.cmd == "sample_data":
        step_sample_data()
    elif args.cmd == "embed":
        step_embed()
    elif args.cmd == "index":
        step_index()
    elif args.cmd == "search":
        step_search(args.query, args.top_k)
    elif args.cmd == "compare":
        step_compare()
    elif args.cmd == "ori":
        step_ori_optimization()

if __name__ == "__main__":
    main()
