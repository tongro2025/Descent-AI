# Real Environment Execution Guide

## 🚀 Step 1: GCP Project Setup

### 1.1 Create GCP Project
```bash
# Create new project in Google Cloud Console
# Or use existing project
# Record the project ID (e.g., my-descent-project-123)
```

### 1.2 Enable Required APIs
```bash
# Enable BigQuery API
gcloud services enable bigquery.googleapis.com

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable Cloud Resource Manager API (if needed)
gcloud services enable cloudresourcemanager.googleapis.com
```

### 1.3 Authentication Setup
```bash
# Login to Google Cloud
gcloud auth login

# Set default project
gcloud config set project YOUR_PROJECT_ID

# Set application default credentials
gcloud auth application-default login
```

## 🔧 Step 2: Environment Configuration

### 2.1 Copy Environment Template
```bash
cp env.example .env
```

### 2.2 Configure Environment Variables
Edit `.env` file:
```bash
# Required: Your Google Cloud Project ID
GCP_PROJECT=your-actual-project-id

# BigQuery Configuration
BQ_DATASET=descent_demo
BQ_LOCATION=US

# Optional: Google Cloud Storage
GCS_BUCKET=gs://your-bucket-name

# Embedding Model Configuration
USE_REAL_EMBEDDINGS=true
EMBEDDING_MODEL=models.text_embedding
USE_MULTIMODAL=false

# ORI Algorithm Parameters
ORI_WEIGHT=0.7
ORI_THRESHOLD=0.3

# Performance Settings
TOP_K_RESULTS=10
BATCH_SIZE=1000
```

## 📦 Step 3: Dependencies Installation

### 3.1 Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3.2 Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 3.3 Verify Installation
```bash
# Test imports
python -c "import google.cloud.bigquery; import vertexai; print('Dependencies OK')"
```

## 🗄️ Step 4: BigQuery Dataset Setup

### 4.1 Initialize Dataset
```bash
# Create dataset and tables
python descent_cli.py init --project-id YOUR_PROJECT_ID --dataset-id descent_demo
```

### 4.2 Verify Dataset Creation
```bash
# Check in BigQuery console or run:
bq ls YOUR_PROJECT_ID:descent_demo
```

## 📊 Step 5: Data Loading

### 5.1 Load Sample Data
```bash
# Load sample text and structured data
python descent_cli.py sample-data
```

### 5.2 Verify Data Loading
```sql
-- Check raw_texts table
SELECT * FROM `YOUR_PROJECT_ID.descent_demo.raw_texts` LIMIT 5;

-- Check feat_struct table
SELECT * FROM `YOUR_PROJECT_ID.descent_demo.feat_struct` LIMIT 5;
```

## 🤖 Step 6: Embedding Generation

### 6.1 Generate Text Embeddings
```bash
# Generate embeddings using Vertex AI
python descent_cli.py embed --mode vertex --dry-run False
```

### 6.2 Generate Structured Embeddings
```bash
# Generate structured feature embeddings
python descent_cli.py embed --mode structured
```

### 6.3 Verify Embeddings
```sql
-- Check text embeddings
SELECT id, ARRAY_LENGTH(embedding) as dims 
FROM `YOUR_PROJECT_ID.descent_demo.emb_view_t_vertex` 
LIMIT 5;

-- Check structured embeddings
SELECT id, ARRAY_LENGTH(features) as dims 
FROM `YOUR_PROJECT_ID.descent_demo.feat_struct_vec` 
LIMIT 5;
```

## 🔍 Step 7: Vector Search Setup

### 7.1 Create Vector Index
```bash
# Create vector index for fast search
python descent_cli.py index
```

### 7.2 Test Vector Search
```bash
# Run vector search test
python descent_cli.py search --query "high performance GPU"
```

## 📈 Step 8: ORI Analysis

### 8.1 Run ORI Analysis
```bash
# Execute ORI discrepancy detection
python descent_cli.py ori --weight 0.7 --threshold 0.3
```

### 8.2 View Results
```sql
-- Check ORI results
SELECT * FROM `YOUR_PROJECT_ID.descent_demo.ori_results` 
ORDER BY ori_score DESC 
LIMIT 10;
```

## 📊 Step 9: Performance Evaluation

### 9.1 Generate Evaluation Report
```bash
# Generate comprehensive evaluation report
python descent_cli.py report --modes text multimodal native
```

### 9.2 View Performance Metrics
```sql
-- Check evaluation metrics
SELECT * FROM `YOUR_PROJECT_ID.descent_demo.eval_metrics`;
```

## 🎯 Step 10: Full Pipeline Test

### 10.1 Run Complete Pipeline
```bash
# Execute full pipeline
make all
```

### 10.2 Validate Results
```bash
# Validate pipeline results
python scripts/validate_pipeline.py
```

## 📁 Expected Output Structure

After successful execution:

```
artifacts/
├── evaluation_report.md
├── multimodal_evidence_report.md
├── performance_metrics.json
└── bq_capture_summary.md

reports/
├── accurate_performance_table.html
├── accurate_performance_table.md
└── evaluation_results.json
```

## 🔧 Troubleshooting

### Common Issues and Solutions:

1. **Authentication Errors**
   ```bash
   # Re-authenticate
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Permission Denied**
   ```bash
   # Check IAM roles
   gcloud projects get-iam-policy YOUR_PROJECT_ID
   ```

3. **API Not Enabled**
   ```bash
   # Enable required APIs
   gcloud services enable bigquery.googleapis.com aiplatform.googleapis.com
   ```

4. **Dataset Already Exists**
   ```bash
   # The system handles existing datasets gracefully
   # No action needed
   ```

5. **Memory Issues**
   ```bash
   # Reduce batch size in .env
   BATCH_SIZE=100
   ```

## 🚀 Production Deployment

### For Production Use:

1. **Set up proper IAM roles**
2. **Configure monitoring and logging**
3. **Set up cost alerts**
4. **Implement error handling**
5. **Schedule regular maintenance**

## 📞 Support

If you encounter issues:

1. Check the logs in `logs/` directory
2. Review the troubleshooting section above
3. Check BigQuery console for error messages
4. Verify your GCP project permissions

---

**Ready for production!** Your multimodal discrepancy detection system is now fully operational. 🎉