#!/usr/bin/env python3
"""
실제 오픈소스 임베딩 생성 및 저장
"""

from google.cloud import bigquery
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    project_id = os.getenv('GCP_PROJECT')
    dataset_id = os.getenv('BQ_DATASET', 'descent_demo')

    print('🧠 실제 오픈소스 임베딩 생성 시작...')
    print(f'프로젝트: {project_id}, 데이터셋: {dataset_id}')

    # 모델 로드
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print(f'✅ 모델 로드 완료 (차원: {model.get_sentence_embedding_dimension()})')

    # BigQuery 클라이언트
    client = bigquery.Client(project=project_id)

    # 텍스트 데이터 조회
    query = f'SELECT id, body FROM `{project_id}.{dataset_id}.raw_texts`'
    rows = list(client.query(query).result())
    print(f'📊 {len(rows)}개 텍스트 발견')

    # 임베딩 생성
    embeddings_data = []
    for row in rows:
        embedding = model.encode(row.body).tolist()
        embeddings_data.append({'id': row.id, 'embedding': embedding})
        print(f'  ✅ {row.id}: {len(embedding)}차원 임베딩 생성')

    print('✅ 모든 임베딩 생성 완료!')
    
    # BigQuery에 저장
    schema = [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("embedding", "FLOAT64", mode="REPEATED"),
    ]
    
    table_id = f"{project_id}.{dataset_id}.emb_view_t"
    job_config = bigquery.LoadJobConfig(schema=schema)
    
    print(f'💾 BigQuery에 저장 중: {table_id}')
    job = client.load_table_from_json(embeddings_data, table_id, job_config=job_config)
    job.result()
    
    print('🎉 실제 임베딩 저장 완료!')
    
    # 결과 확인
    result_query = f"""
    SELECT 
      id,
      ARRAY_LENGTH(embedding) as embedding_dim,
      embedding[OFFSET(0)] as first_value,
      embedding[OFFSET(1)] as second_value
    FROM `{project_id}.{dataset_id}.emb_view_t`
    ORDER BY id
    """
    
    results = client.query(result_query).to_dataframe()
    
    print('\n📊 실제 임베딩 결과:')
    print('=' * 50)
    for _, row in results.iterrows():
        print(f'ID: {row["id"]}')
        print(f'차원: {row["embedding_dim"]}')
        print(f'첫 번째 값: {row["first_value"]:.6f}')
        print(f'두 번째 값: {row["second_value"]:.6f}')
        print('-' * 30)

if __name__ == "__main__":
    main()
