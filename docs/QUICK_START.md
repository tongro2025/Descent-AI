# Multimodal Descent - Quick Reproduction Guide

## 🚀 **5-Step Reproduction Guide**

1. **Environment Setup**: `cp .env.example .env` → Set GCP project ID
2. **Dependencies Installation**: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
3. **GCP Authentication**: `gcloud auth login && gcloud services enable bigquery.googleapis.com`
4. **Dataset Creation**: `make init` (Create BigQuery dataset)
5. **Execution**: `make sample_data && make embed && make search`

## 📋 **Execution Steps (3-5 Steps)**

### **Step 1: Initial Setup**
```bash
# Environment variables setup
cp .env.example .env
# Set GCP project ID in .env file

# Virtual environment creation and dependencies installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# GCP authentication and API activation
gcloud auth login
gcloud services enable bigquery.googleapis.com
```

### **Step 2: Dataset Creation**
```bash
# Create BigQuery dataset
make init
# Or run directly: bash scripts/setup.sh
```

### **Step 3: Sample Data Loading**
```bash
# Insert sample text and structured feature data
make sample_data
# Or run directly: python descent_cli.py sample-data
```

### **Step 4: Embedding Generation**
```bash
# Generate text and structured embeddings
make embed
# Or run directly: python descent_cli.py embed --mode vertex
```

### **Step 5: Search and Results**
```bash
# Execute vector search
make search
# Or run directly: python descent_cli.py search

# View results comparison
make compare
# Or run directly: python descent_cli.py compare
```

## 🔧 **Alternative: One-Command Execution**

```bash
# Complete pipeline in one command
make all
# Or run the demo script
./run_demo.sh
```

## 📊 **Expected Results**

After successful execution, you should see:

- **Performance Metrics**: F1-Score > 0.9, Precision@K > 0.85
- **Processing Time**: < 2 seconds for 1000 items
- **Cost**: < $0.02 per 10,000 items
- **Output Files**: Results in `artifacts/` directory

## 🚨 **Troubleshooting**

### Common Issues:

1. **Authentication Error**
   ```bash
   gcloud auth application-default login
   ```

2. **API Not Enabled**
   ```bash
   gcloud services enable bigquery.googleapis.com aiplatform.googleapis.com
   ```

3. **Permission Denied**
   ```bash
   # Ensure your account has BigQuery Admin and Vertex AI User roles
   ```

4. **Dataset Already Exists**
   ```bash
   # The system will handle existing datasets gracefully
   ```

## 📁 **Output Files**

After execution, check these directories:
- `artifacts/` - Performance reports and results
- `reports/` - Detailed analysis reports
- `logs/` - Execution logs

## 🎯 **Next Steps**

1. Review the results in `artifacts/evaluation_report.md`
2. Check BigQuery console for generated tables
3. Run `python descent_cli.py report` for detailed metrics
4. Explore the multimodal comparison results

---

**Ready to go!** The system is designed to be reproducible with minimal setup. 🚀