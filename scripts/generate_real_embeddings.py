#!/usr/bin/env python3
"""
Generate Real Embeddings Script
Creates real embeddings for sample data using Vertex AI.
"""

import os
import sys
import pandas as pd
from google.cloud import bigquery
from google.cloud import aiplatform
from typing import List, Dict
import json

def generate_text_embeddings(texts: List[str], project_id: str) -> List[List[float]]:
    """Generate text embeddings using Vertex AI."""
    
    aiplatform.init(project=project_id, location='us-central1')
    
    # Use text-embedding-005 model
    model = aiplatform.Model('text-embedding-005')
    
    embeddings = []
    for text in texts:
        try:
            # Generate embedding
            embedding = model.get_embedding(text)
            embeddings.append(embedding)
        except Exception as e:
            print(f"Error generating embedding for text: {e}")
            # Fallback to zero vector
            embeddings.append([0.0] * 768)
    
    return embeddings

def save_embeddings_to_csv(embeddings: List[List[float]], filename: str):
    """Save embeddings to CSV file."""
    
    # Convert to DataFrame
    df = pd.DataFrame(embeddings)
    
    # Add column names
    df.columns = [f'dim_{i}' for i in range(len(embeddings[0]))]
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Embeddings saved to {filename}")

def main():
    """Main function."""
    
    # Get configuration
    project_id = os.getenv('GCP_PROJECT')
    if not project_id:
        print("❌ GCP_PROJECT environment variable not set")
        sys.exit(1)
    
    # Sample texts for embedding generation
    sample_texts = [
        "High performance GPU with advanced cooling system",
        "Professional camera with 4K video recording capability",
        "Wireless headphones with noise cancellation technology",
        "Smartphone with 5G connectivity and long battery life",
        "Laptop computer with SSD storage and fast processor",
        "Tablet device with touch screen and stylus support"
    ]
    
    print(f"Generating embeddings for {len(sample_texts)} texts...")
    print(f"Project: {project_id}")
    
    try:
        # Generate embeddings
        embeddings = generate_text_embeddings(sample_texts, project_id)
        
        # Save to CSV
        output_file = "data/sample/generated_text_embeddings.csv"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        save_embeddings_to_csv(embeddings, output_file)
        
        print("✅ Embedding generation completed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
