# Descent: Multimodal Discrepancy Detection System

A championship-level multimodal AI system for detecting discrepancies across text, image, and structured data using Google Cloud BigQuery AI and Vertex AI.

## 🔗 Quick Links

- 🧠 **Writeup**: [Kaggle Writeup](docs/KAGGLE_WRITEUP.md)
- 💻 **GitHub**: https://github.com/tongro2025/Descent-AI
- 🎬 **Demo Video**: [YouTube Demo](https://youtu.be/PX92XztRlSQ)
- 📦 **Submission Bundle**: See `reports/` & `artifacts/` directories
- 📄 **License**: CC BY 4.0 (per competition rules; commercial use permitted)

## 📋 Data Preparation

**⚠️ IMPORTANT: Competition data is not included in this repository.**

To reproduce the results, you need to:

1. **Download competition data** from Kaggle (following competition rules)
2. **Place data files** in the `data/` directory:
   - `raw_texts.csv` - Product descriptions and manuals
   - `feat_struct.csv` - Structured features
   - `struct_embeddings.csv` - Pre-computed embeddings
   - `text_embeddings.csv` - Text embeddings

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your GCP project details
   ```

4. **Run the pipeline**:
   ```bash
   python descent_cli.py run --mode vertex
   ```

## 🏆 Key Features

- **3 Embedding Options**: Vertex AI, Open Source, Native BigQuery AI
- **Real Multimodal Integration**: Text (768D) + Image (1408D) + Structured (3D) = 2179D
- **100% Recall**: Perfect recall on labeled mismatches (with large F1 and latency/cost wins)
- **Production Ready**: Dry run, retry logic, cost monitoring
- **Complete Automation**: CLI + Makefile for full automation

## 🚀 Quick Start

### Prerequisites

- Google Cloud Project with BigQuery and Vertex AI enabled
- Python 3.8+
- Google Cloud SDK installed and authenticated

**Enable required APIs:**
```bash
gcloud services enable bigquery.googleapis.com aiplatform.googleapis.com
```

### Environment Setup

1. **Copy environment template**:
   ```bash
   cp env.example .env
   ```

2. **Configure your environment**:
   Edit `.env` file with your actual values:
   ```bash
   # Required: Your Google Cloud Project ID
   GCP_PROJECT=your-actual-project-id
   
   # Optional: Customize other settings
   BQ_DATASET=descent_demo
   BQ_LOCATION=US
   USE_REAL_EMBEDDINGS=true
   USE_MULTIMODAL=false
   ```

3. **Set up Google Cloud authentication**:
   ```bash
   gcloud auth login
   gcloud config set project your-actual-project-id
   ```

### Installation

```bash
# Clone the repository
git clone https://github.com/tongro2025/Descent-AI.git
cd Descent-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize project
python descent_cli.py init --project-id YOUR_PROJECT_ID --dataset-id descent_demo
```

### Basic Usage

```bash
# Generate embeddings
python descent_cli.py embed

# Run ORI analysis
python descent_cli.py ori --weight 0.7 --threshold 0.3

# Generate evaluation report
python descent_cli.py report --modes text multimodal native

# Run integration tests
python descent_cli.py test --test-mode mini
```

## 🎯 Architecture

### Embedding Options

1. **Option A: Native BigQuery AI**
   - Uses `ML.GENERATE_EMBEDDING` (e.g., model='text-embedding-005')
   - Direct SQL-based embedding generation
   - Requires BigQuery AI permissions

2. **Option B: Vertex AI Python SDK**
   - Uses `text-embedding-005` model (768 dimensions)
   - Python-based embedding generation
   - Uploads to BigQuery for analysis

3. **Option C: Open Source Models**
   - Uses SentenceTransformers `all-MiniLM-L6-v2` (384 dimensions)
   - Local embedding generation
   - Fallback option for testing

### Multimodal Integration

- **Text Embeddings**: Vertex AI text-embedding-005 (768D)
- **Image Embeddings**: Vertex AI multimodalembedding@001 (1408D)
- **Structured Features**: Z-score normalized (3D)
- **Combined**: ARRAY_CONCAT for multimodal fusion (2179D)

Example SQL:
```sql
SELECT ARRAY_CONCAT(t.text_vec, i.image_vec, s.struct_vec) AS emb_stitched FROM ...
```

### ORI Algorithm

The ORI (Discrepancy Index) algorithm combines:
- **Semantic Distance**: Cosine similarity between embeddings
- **Rule-based Score**: Keyword matching for discrepancy terms
- **Weighted Combination**: `ORI = w * semantic_distance + (1-w) * rule_score`

## 📊 Performance Results

| Metric | Keyword Search | Descent AI | Improvement |
|--------|----------------|------------|-------------|
| **Accuracy** | 33% | 50% | +51.5% |
| **Precision** | 31% | 50% | +61.3% |
| **Recall** | 25% | 100% | +300% |
| **F1 Score** | 28% | 66.7% | +138.2% |
| **Processing Time** | 5 min | 1.22 s | -99.8% |
| **Cost / 10k items** | $500 | $0.018 | -99.6% |

## 🛠️ Advanced Usage

### Configuration

Edit `config.yaml` to customize settings:

```yaml
project_id: "your-project-id"
dataset_id: "descent_demo"
location: "US"
mode: "vertex"  # vertex, oss, native
dry_run: false
ori_weight: 0.7
ori_threshold: 0.3
```

### CLI Commands

```bash
# Project management
python descent_cli.py init --project-id PROJECT_ID
python descent_cli.py status
python descent_cli.py clean

# Pipeline execution
python descent_cli.py embed --dry-run
python descent_cli.py stitch
python descent_cli.py ori --weight 0.8 --threshold 0.2

# Evaluation and reporting
python descent_cli.py report --output-format markdown
python descent_cli.py test --test-mode full

# Development tools
make install
make lint
make format
make bundle
```

### Makefile Commands

```bash
# Basic operations
make init          # Initialize project
make embed         # Generate embeddings
make stitch        # Multimodal stitching
make ori           # ORI analysis
make report        # Generate evaluation report
make test          # Integration tests

# Development
make install       # Install dependencies
make lint          # Code linting
make format        # Code formatting
make bundle        # Create submission bundle

# CI/CD
make ci-test       # CI tests
make ci-report     # CI reports
```

## 📁 Project Structure

```
Descent-AI/
├── 📄 Core Files
│   ├── README.md                    # Project overview and usage guide
│   ├── PROJECT_STRUCTURE.md         # Detailed project structure
│   ├── config.yaml                  # Main configuration
│   ├── Makefile                     # Build automation
│   └── requirements.txt             # Python dependencies
│
├── 🐍 Source Code (src/descent/)
│   ├── descent_cli.py               # Command-line interface
│   ├── descent_pipeline_v2.py       # Core pipeline engine (319 lines)
│   ├── bq.py                        # BigQuery client wrapper
│   ├── config.py                    # Configuration management
│   └── eval_harness.py              # Evaluation system
│
├── 🗄️ SQL Scripts (22 files)
│   ├── 01_schema.sql                # Database schema
│   ├── 02_embeddings.sql            # Embedding generation
│   ├── 03_incremental_idempotency.sql # Incremental processing
│   ├── 05_sample_data.sql           # Sample data insertion
│   ├── 08_create_vector_index.sql   # Vector index creation
│   ├── 12_ori_optimization.sql      # ORI algorithm optimization
│   └── ...                          # 16 additional SQL scripts
│
├── 📚 Documentation (docs/)
│   ├── ARCHITECTURE.md              # System architecture
│   ├── QUICK_START.md               # Quick reproduction guide
│   ├── REAL_ENVIRONMENT_GUIDE.md    # Production setup
│   ├── KAGGLE_WRITEUP.md            # Competition writeup
│   └── ...                          # 6 additional guides
│
├── 📊 Reports & Results (reports/)
│   ├── evaluation_report.md         # Comprehensive evaluation
│   ├── multimodal_evidence_report.md # Multimodal proof
│   ├── performance_measurement_results.json # Performance data
│   └── ...                          # 6 additional reports
│
├── 📈 Sample Data (data/sample/)
│   ├── raw_texts.csv                # Sample text data
│   ├── feat_struct.csv              # Sample structured features
│   ├── text_embeddings.csv          # Sample text embeddings
│   └── struct_embeddings.csv        # Sample structured embeddings
│
└── 🛠️ Tools & Scripts
    ├── run_demo.sh                  # Complete demo script
    ├── scripts/validate_pipeline.py # Pipeline validation
    ├── scripts/check_gitignore.sh   # Security verification
    └── artifacts/                   # Generated outputs
```

**📋 Detailed Structure**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete file inventory.

## 🔧 Technical Details

### BigQuery Schema

- `raw_texts`: Source text data with content hashing
- `emb_view_t_vertex`: Vertex AI text embeddings (768D)
- `emb_view_i_real`: Vertex AI image embeddings (1408D)
- `feat_struct_vec`: Structured feature vectors (3D)
- `emb_stitched_real`: Multimodal combined embeddings (2179D)
- `report_ori`: ORI analysis results
- `eval_metrics`: Performance evaluation metrics

### Key Technologies

- **Google Cloud BigQuery**: Data warehouse and SQL processing
- **Vertex AI**: Google's ML platform for embeddings
- **BigQuery AI**: Native AI functions in BigQuery
- **SentenceTransformers**: Open source embedding models
- **Python**: Pipeline orchestration and data processing
- **Typer**: Modern CLI framework
- **Pandas**: Data manipulation and analysis

## 🎬 Demo Materials

### CLI Demo
```bash
./run_demo.sh  # Complete CLI demonstration
```

### BigQuery Screenshots
- `artifacts/01_basic_data.sql` - Basic data verification
- `artifacts/02_text_embeddings.sql` - Text embedding results
- `artifacts/03_image_embeddings.sql` - Image embedding results
- `artifacts/04_ori_results.sql` - ORI analysis results
- `artifacts/05_multimodal_comparison.sql` - Multimodal comparison
- `artifacts/06_embedding_dimensions.sql` - Dimension comparison
- `artifacts/07_evaluation_metrics.sql` - Performance metrics
- `artifacts/08_multimodal_stitched.sql` - Multimodal integration

### Evidence Materials
- `artifacts/multimodal_evidence_report.md` - Multimodal proof
- `artifacts/evaluation_report.md` - Performance evaluation
- `artifacts/bq_capture_summary.md` - BigQuery results summary

## 🏅 Championship Features

### P0: Reliability & Reproducibility
- ✅ Dry run + Idempotency
- ✅ Error handling & retry logic
- ✅ Unified configuration (config.yaml)
- ✅ Schema versioning

### P1: Performance & Scale
- ✅ Incremental embedding
- ✅ Hash-based idempotency
- ✅ Partitioning & clustering
- ✅ Cost monitoring

### P2: Quality & Validation
- ✅ Evaluation harness
- ✅ Externalized ORI parameters
- ✅ Cost reporting
- ✅ Performance metrics

### P3: Code & CI/CD
- ✅ CLI integration
- ✅ Test & linting
- ✅ Makefile automation
- ✅ Documentation

## 📈 Business Impact

- **Recall**: 100% on labeled mismatches (with large F1 and latency/cost wins)
- **Efficiency**: Automated pipeline reduces manual effort
- **Scalability**: Handles large datasets with incremental processing
- **Reliability**: Production-ready with error handling
- **Flexibility**: Multiple embedding options for different scenarios

## 🔒 Security & Privacy

### Data Protection
- **No sensitive data**: This repository contains no actual competition data
- **Environment variables**: All sensitive configuration is externalized
- **Git ignore**: Sensitive files are automatically excluded from version control
- **Security warning**: Never commit .env files or service account keys. Use .env.example as template only.

### Safe Configuration
```bash
# Never commit these files:
.env
*.key
service-account*.json
credentials.json
```

### Compliance
- **CC BY 4.0 License**: Ensures commercial use is permitted
- **Open Source**: All dependencies use permissive licenses
- **No proprietary data**: Only uses publicly available datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

## 📄 License

This project is licensed under the Creative Commons Attribution 4.0 International License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud BigQuery AI team
- Vertex AI platform
- SentenceTransformers community
- Kaggle BigQuery AI Hackathon organizers

## 🚀 One-line Recipes

```bash
# Quick start
python descent_cli.py run --mode vertex --dry-run False

# Generate report
python descent_cli.py report --modes text multimodal native

# Test with sample data
python descent_cli.py test --test-mode mini
```

---

**Descent**: Where multimodal AI meets championship-level engineering 🏆