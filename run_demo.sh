#!/bin/bash

# Descent AI Demo Script
# This script demonstrates the complete pipeline with sample data

echo "🚀 Starting Descent AI Demo..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Please copy env.example to .env and configure it."
    exit 1
fi

# Load environment variables
source .env

echo "📋 Demo Steps:"
echo "1. Initialize project..."
python descent_cli.py init --project-id $GCP_PROJECT --dataset-id $BQ_DATASET

echo "2. Generate embeddings with sample data..."
python descent_cli.py embed --mode vertex --dry-run False

echo "3. Run ORI analysis..."
python descent_cli.py ori --weight 0.7 --threshold 0.3

echo "4. Generate evaluation report..."
python descent_cli.py report --modes text multimodal native

echo "✅ Demo completed! Check the artifacts/ directory for results."
