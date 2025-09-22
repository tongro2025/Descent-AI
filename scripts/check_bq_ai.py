#!/usr/bin/env python3
"""
BigQuery AI Functions Checker
Verifies that required BigQuery AI functions are available and working.
"""

import os
import sys
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest

def check_bigquery_ai_functions(project_id, dataset_id):
    """Check if BigQuery AI functions are available."""
    
    client = bigquery.Client(project=project_id)
    
    print(f"Checking BigQuery AI functions for project: {project_id}")
    print(f"Dataset: {dataset_id}")
    print("-" * 50)
    
    # Test ML.GENERATE_EMBEDDING
    try:
        query = f"""
        SELECT ML.GENERATE_EMBEDDING(
            MODEL 'text-embedding-005',
            STRUCT('test content' AS content)
        ) AS embedding
        LIMIT 1
        """
        
        result = client.query(query)
        rows = list(result)
        
        if rows:
            embedding = rows[0].embedding
            print(f"✅ ML.GENERATE_EMBEDDING: Working (dimension: {len(embedding)})")
        else:
            print("❌ ML.GENERATE_EMBEDDING: No results returned")
            
    except BadRequest as e:
        print(f"❌ ML.GENERATE_EMBEDDING: {e}")
    except Exception as e:
        print(f"❌ ML.GENERATE_EMBEDDING: Unexpected error - {e}")
    
    # Test VECTOR_SEARCH (if table exists)
    try:
        table_id = f"{project_id}.{dataset_id}.test_embeddings"
        
        # Check if table exists first
        try:
            table = client.get_table(table_id)
            print(f"✅ Test table exists: {table_id}")
            
            query = f"""
            SELECT VECTOR_SEARCH(
                TABLE `{table_id}`,
                'embedding',
                (SELECT ML.GENERATE_EMBEDDING(
                    MODEL 'text-embedding-005',
                    STRUCT('test query' AS content)
                )),
                top_k => 5
            ) AS results
            LIMIT 1
            """
            
            result = client.query(query)
            rows = list(result)
            
            if rows:
                print("✅ VECTOR_SEARCH: Working")
            else:
                print("❌ VECTOR_SEARCH: No results returned")
                
        except NotFound:
            print(f"⚠️  VECTOR_SEARCH: Test table {table_id} not found (this is OK for initial check)")
            
    except BadRequest as e:
        print(f"❌ VECTOR_SEARCH: {e}")
    except Exception as e:
        print(f"❌ VECTOR_SEARCH: Unexpected error - {e}")
    
    print("-" * 50)
    print("BigQuery AI functions check completed.")

def main():
    """Main function."""
    
    # Get configuration from environment
    project_id = os.getenv('GCP_PROJECT')
    dataset_id = os.getenv('BQ_DATASET', 'descent_demo')
    
    if not project_id:
        print("❌ GCP_PROJECT environment variable not set")
        print("Please set GCP_PROJECT in your .env file")
        sys.exit(1)
    
    try:
        check_bigquery_ai_functions(project_id, dataset_id)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
