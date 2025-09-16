#!/bin/bash
# Single Command for Descent Pipeline Demo
# Run this one command in iTerm (after cd /Users/hakjun/Desktop/Descent)

echo "🎬 Starting Descent Pipeline Demo"
echo "=================================="

# Activate virtual environment
source venv/bin/activate

# Check system status
echo "📊 1. System Status Check"
python3 descent_cli.py status
echo ""

# Initialize project
echo "🚀 2. Project Initialization"
python3 descent_cli.py init --project-id gen-lang-client-0790720774 --dataset-id descent_demo --mode vertex
echo ""

# Dry run test
echo "🧪 3. Dry Run Test"
python3 descent_cli.py embed --dry-run
echo ""

# ORI analysis
echo "🎯 4. ORI Analysis"
python3 descent_cli.py ori --weight 0.7 --threshold 0.3
echo ""

# Generate evaluation report
echo "📊 5. Evaluation Report Generation"
python3 descent_cli.py report --modes text multimodal native --output-format markdown
echo ""

# Integration test
echo "🧪 6. Integration Test"
python3 descent_cli.py test --test-mode mini
echo ""

# Check artifacts
echo "📁 7. Artifacts Check"
ls -la artifacts/
echo ""

# View evaluation report
echo "📋 8. Evaluation Report"
cat artifacts/evaluation_report.md
echo ""

# View multimodal evidence
echo "🔗 9. Multimodal Evidence"
cat artifacts/multimodal_evidence_report.md
echo ""

# Check BigQuery results
echo "📊 10. BigQuery Results"
echo "Text Embeddings:"
head -5 artifacts/bq_results_text_embeddings.csv
echo ""
echo "Image Embeddings:"
head -5 artifacts/bq_results_image_embeddings.csv
echo ""
echo "Embedding Dimensions:"
cat artifacts/bq_results_embedding_dimensions.csv
echo ""

# Show performance metrics
echo "📈 11. Performance Metrics"
cat artifacts/evaluation_comparison.csv
echo ""

# Create final bundle
echo "📦 12. Final Bundle Creation"
make bundle
echo ""

# Check final submission
echo "✅ 13. Final Submission Check"
ls -la descent_submission.zip
echo ""

echo "🎉 Demo completed! Ready for Kaggle submission!"
echo "File: descent_submission.zip"
echo "Size: $(ls -lh descent_submission.zip | awk '{print $5}')"
