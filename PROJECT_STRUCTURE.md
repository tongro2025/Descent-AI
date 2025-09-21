# Project Structure

This document provides a comprehensive overview of the Descent AI project structure.

## 📁 Directory Structure

```
Descent-AI/
├── 📄 Core Configuration
│   ├── README.md                    # Project overview and usage guide
│   ├── LICENSE                      # CC BY 4.0 license
│   ├── .gitignore                   # Git ignore rules for security
│   ├── requirements.txt             # Python dependencies
│   ├── config.yaml                  # Main configuration file
│   ├── Makefile                     # Build automation commands
│   └── env.example                  # Environment variables template
│
├── 🐍 Source Code
│   └── src/descent/
│       ├── __init__.py              # Package initialization
│       ├── descent_cli.py           # Command-line interface
│       ├── descent_pipeline_v2.py   # Main pipeline engine (319 lines)
│       ├── bq.py                    # BigQuery client wrapper
│       ├── config.py                # Configuration management
│       └── eval_harness.py          # Evaluation system
│
├── 🗄️ Database Scripts
│   └── sql/
│       ├── 01_schema.sql            # Database schema definition
│       ├── 02_embeddings.sql        # Embedding generation
│       ├── 03_incremental_idempotency.sql # Incremental processing
│       ├── 04_search_demo.sql       # Search demonstration
│       ├── 05_sample_data.sql       # Sample data insertion
│       ├── 06_before_after.sql      # Before/after comparison
│       ├── 07_evaluation_metrics.sql # Performance metrics
│       ├── 08_create_vector_index.sql # Vector index creation
│       ├── 09_vector_search.sql     # Vector search queries
│       ├── 10_before_after_comparison.sql # Detailed comparison
│       ├── 11_local_simulation.sql  # Local testing simulation
│       ├── 12_ori_optimization.sql  # ORI algorithm optimization
│       ├── create_reports.sql       # Report generation
│       └── rebuild_stitched.sql     # Multimodal stitching rebuild
│
├── 📚 Documentation
│   └── docs/
│       ├── ARCHITECTURE.md          # System architecture overview
│       ├── BIGQUERY_CONSOLE_QUERIES.md # BigQuery console queries
│       ├── IMPACT_REPORT.md         # Business impact analysis
│       ├── KAGGLE_WRITEUP.md        # Kaggle competition writeup
│       ├── QUICK_START.md           # Quick reproduction guide
│       ├── REAL_ENVIRONMENT_GUIDE.md # Production environment setup
│       ├── SCREENSHOT_GUIDE.md      # Screenshot capture guide
│       ├── SCREENSHOT_CAPTURE_GUIDE.md # Detailed screenshot guide
│       ├── SCREENSHOTS_README.md    # Screenshots documentation
│       └── SUBMISSION_CHECKLIST.md  # Pre-submission checklist
│
├── 📊 Reports & Results
│   └── reports/
│       ├── accurate_extended_writeup.md # Extended technical writeup
│       ├── accurate_performance_table.html # Performance table (HTML)
│       ├── accurate_performance_table.md # Performance table (Markdown)
│       ├── bq_capture_summary.md    # BigQuery results summary
│       ├── evaluation_report.md     # Comprehensive evaluation report
│       ├── evaluation_results.json  # Evaluation metrics (JSON)
│       ├── multimodal_evidence_report.md # Multimodal proof of concept
│       ├── performance_measurement_report.md # Performance analysis
│       └── performance_measurement_results.json # Performance data (JSON)
│
├── 🛠️ Scripts & Tools
│   └── scripts/
│       ├── check_bq_ai.py           # BigQuery AI availability check
│       ├── generate_real_embeddings.py # Real embedding generation
│       ├── setup.sh                 # Environment setup script
│       └── validate_pipeline.py     # Pipeline validation script
│
├── 📈 Sample Data
│   └── data/sample/
│       ├── feat_struct.csv          # Sample structured features
│       ├── raw_texts.csv            # Sample text data
│       ├── struct_embeddings.csv    # Sample structured embeddings
│       └── text_embeddings.csv      # Sample text embeddings
│
├── 🎬 Demo & Execution
│   ├── run_demo.sh                  # Complete demo script
│   ├── check_gitignore.sh           # Git ignore verification script
│   └── measure_performance.py       # Performance measurement tool
│
├── 📦 Artifacts (Generated)
│   └── artifacts/                   # Generated results and outputs
│
└── 📝 Logs (Generated)
    └── logs/                        # Execution logs
```

## 🔧 File Categories

### Core Files
- **Configuration**: `config.yaml`, `env.example`, `requirements.txt`
- **Build**: `Makefile`, `run_demo.sh`
- **Documentation**: `README.md`, `LICENSE`, `PROJECT_STRUCTURE.md`

### Source Code
- **Main Pipeline**: `descent_pipeline_v2.py` (319 lines)
- **CLI Interface**: `descent_cli.py`
- **Database Client**: `bq.py`
- **Evaluation**: `eval_harness.py`

### SQL Scripts (22 files)
- **Schema**: `01_schema.sql`
- **Embeddings**: `02_embeddings*.sql` (4 variants)
- **Processing**: `03_*.sql`, `04_*.sql`, `05_*.sql`
- **Analysis**: `06_*.sql`, `07_*.sql`, `08_*.sql`
- **Search**: `09_*.sql`, `10_*.sql`, `11_*.sql`
- **Optimization**: `12_*.sql`
- **Utilities**: `create_reports.sql`, `rebuild_stitched.sql`

### Documentation (10 files)
- **Architecture**: `ARCHITECTURE.md`
- **Guides**: `QUICK_START.md`, `REAL_ENVIRONMENT_GUIDE.md`
- **Competition**: `KAGGLE_WRITEUP.md`, `SUBMISSION_CHECKLIST.md`
- **Technical**: `BIGQUERY_CONSOLE_QUERIES.md`, `IMPACT_REPORT.md`
- **Screenshots**: `SCREENSHOT_*.md`, `SCREENSHOTS_README.md`

### Reports & Results (9 files)
- **Performance**: `accurate_performance_table.*`, `performance_measurement_*`
- **Evaluation**: `evaluation_report.md`, `evaluation_results.json`
- **Technical**: `accurate_extended_writeup.md`, `multimodal_evidence_report.md`
- **Summary**: `bq_capture_summary.md`

### Scripts & Tools (4 files)
- **Setup**: `setup.sh`
- **Validation**: `validate_pipeline.py`
- **Generation**: `generate_real_embeddings.py`
- **Checking**: `check_bq_ai.py`

### Sample Data (4 files)
- **Text**: `raw_texts.csv`, `text_embeddings.csv`
- **Structured**: `feat_struct.csv`, `struct_embeddings.csv`

## 📊 Statistics

- **Total Files**: 67+ files
- **Source Code**: 6 Python files (1,000+ lines)
- **SQL Scripts**: 22 files
- **Documentation**: 10 Markdown files
- **Reports**: 9 result files
- **Sample Data**: 4 CSV files
- **Scripts**: 4 utility scripts

## 🎯 Key Features

1. **Modular Architecture**: Clear separation of concerns
2. **Comprehensive Documentation**: 10 detailed guides
3. **Production Ready**: Complete CI/CD setup
4. **Sample Data**: Immediate testing capability
5. **Security**: Proper .gitignore and environment management
6. **International**: All documentation in English

## 🚀 Quick Navigation

- **Start Here**: `README.md`
- **Quick Setup**: `docs/QUICK_START.md`
- **Full Setup**: `docs/REAL_ENVIRONMENT_GUIDE.md`
- **Run Demo**: `./run_demo.sh`
- **Check Status**: `./check_gitignore.sh`
- **Build All**: `make all`

---

**This structure ensures maximum clarity, maintainability, and ease of use for both development and production deployment.**
