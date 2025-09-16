#!/bin/bash
# Descent Pipeline Demo Script
# Kaggle submission demo video

echo "🎬 Starting Descent Pipeline Demo"
echo "=================================="

# 1. System status check
echo "📊 1. System Status Check"
python3 descent_cli.py status
sleep 2

# 2. Project initialization
echo "🚀 2. Project Initialization"
python3 descent_cli.py init --project-id gen-lang-client-0790720774 --dataset-id descent_demo --mode vertex
sleep 2

# 3. Dry run mode test
echo "🧪 3. Dry Run Mode Test"
python3 descent_cli.py embed --dry-run
sleep 2

# 4. ORI analysis
echo "🎯 4. ORI Analysis"
python3 descent_cli.py ori --weight 0.7 --threshold 0.3
sleep 2

# 5. Evaluation report generation
echo "📊 5. Evaluation Report Generation"
python3 descent_cli.py report --modes text multimodal native --output-format markdown
sleep 2

# 6. Integration test
echo "🧪 6. Integration Test"
python3 descent_cli.py test --test-mode mini
sleep 2

echo "🎉 Demo completed!"
