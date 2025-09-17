from google.cloud import bigquery
from .config import BQ_LOCATION, GCP_PROJECT

def client() -> bigquery.Client:
    return bigquery.Client(project=GCP_PROJECT, location=BQ_LOCATION)

def run_sql(path: str, params: dict | None = None):
    sql = open(path, "r", encoding="utf-8").read()
    job_config = bigquery.QueryJobConfig()
    if params:
        job_config.query_parameters = [
            bigquery.ScalarQueryParameter(k, "STRING" if isinstance(v,str) else "INT64", v)
            for k, v in params.items()
        ]
    job = client().query(sql, job_config=job_config)
    job.result()
    print(f"[OK] Ran: {path}")

