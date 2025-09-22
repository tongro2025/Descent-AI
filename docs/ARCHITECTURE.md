# Descent AI: Multimodal Architecture

## System Architecture Overview

Descent AI implements a production-grade multimodal discrepancy detection system using Google Cloud BigQuery AI functions, combining text, image, and structured data processing in a unified pipeline.

## Core Architecture Diagram

```mermaid
graph TB
    subgraph "Data Sources"
        A[raw_texts<br/>Product descriptions, manuals]
        B[feat_struct<br/>Structured features]
        C[raw_docs<br/>Images, PDFs]
    end
    
    subgraph "BigQuery AI Functions"
        D[ML.GENERATE_EMBEDDING<br/>text-embedding-005]
        E[VECTOR_SEARCH<br/>Real-time similarity]
        F[Object Tables<br/>Multimodal storage]
    end
    
    subgraph "Embedding Generation"
        G[Text Embeddings<br/>768D vectors]
        H[Image Embeddings<br/>1408D vectors]
        I[Structured Features<br/>3D normalized]
    end
    
    subgraph "Multimodal Fusion"
        J[ARRAY_CONCAT<br/>Text + Image + Structured]
        K[emb_stitched<br/>2179D unified vectors]
    end
    
    subgraph "Vector Search & Indexing"
        L[VECTOR_SEARCH<br/>Real-time similarity calculation]
        M[IVF Index<br/>Inverted File Index]
        N[TREE_AH Index<br/>Approximate Nearest Neighbors]
    end
    
    subgraph "ORI Algorithm"
        O[Semantic Distance<br/>w=0.7 weight]
        P[Rule-based Score<br/>1-w=0.3 weight]
        Q[ORI Score<br/>Risk calculation]
    end
    
    subgraph "Results & Analysis"
        R[Risk Classification<br/>HIGH/MEDIUM/LOW]
        S[Before/After Comparison<br/>Performance metrics]
        T[Discrepancy Detection<br/>Real-time alerts]
    end
    
    A --> D
    B --> E
    C --> F
    
    D --> G
    F --> H
    E --> I
    
    G --> J
    H --> J
    I --> J
    
    J --> K
    K --> L
    K --> M
    K --> N
    
    L --> O
    O --> Q
    P --> Q
    
    Q --> R
    R --> S
    S --> T
    
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#e8f5e8
    style H fill:#e8f5e8
    style I fill:#e8f5e8
    style J fill:#fff3e0
    style K fill:#fff3e0
    style L fill:#ffebee
    style M fill:#ffebee
    style N fill:#ffebee
    style O fill:#e0f2f1
    style P fill:#e0f2f1
    style Q fill:#e0f2f1
    style R fill:#f1f8e9
    style S fill:#f1f8e9
    style T fill:#f1f8e9
```

## Data Flow Sequence

```mermaid
sequenceDiagram
    participant U as User Query
    participant BQ as BigQuery AI
    participant E as Embedding Models
    participant V as Vector Search
    participant O as ORI Algorithm
    participant R as Results
    
    U->>BQ: "Search spec and image discrepancies"
    BQ->>E: Generate text embeddings
    E-->>BQ: Return vectors
    BQ->>V: Execute VECTOR_SEARCH
    V-->>BQ: Similarity scores
    BQ->>O: Calculate ORI (w=0.7, τ=0.3)
    O-->>BQ: Risk classification
    BQ-->>R: Discrepancy detection results
    R-->>U: HIGH/MEDIUM/LOW risk levels
```

## Performance Comparison

```mermaid
graph LR
    subgraph "Baseline Approach"
        A1[Keyword Matching]
        A2[Manual Review]
        A3[F1: 0.28]
        A4[Time: 5 minutes]
    end
    
    subgraph "Descent AI"
        B1[Vector Search]
        B2[Automated Detection]
        B3[F1: 0.67]
        B4[Time: 1.22 seconds]
    end
    
    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3 --> B4
    
    style A3 fill:#ffcdd2
    style A4 fill:#ffcdd2
    style B3 fill:#c8e6c9
    style B4 fill:#c8e6c9
```

## BigQuery AI Functions Integration

### 1. ML.GENERATE_EMBEDDING
```sql
-- Text embedding generation
SELECT ML.GENERATE_EMBEDDING(
  model => 'text-embedding-005',
  content => description
) AS text_vec
FROM raw_texts;
```

### 2. VECTOR_SEARCH
```sql
-- Real-time vector similarity search
SELECT VECTOR_SEARCH(
  query => query_embedding,
  table => 'descent_demo.emb_view_t_vertex',
  options => JSON_OBJECT('top_k' => 10)
) AS results;
```

### 3. Object Tables (Multimodal)
```sql
-- Integrated multimodal embeddings
SELECT ARRAY_CONCAT(
  text_embedding, 
  image_embedding, 
  struct_features
) AS multimodal_vec
FROM emb_stitched_real;
```

## Multimodal Integration Details

### Embedding Dimensions
- **Text**: 768D (Vertex AI text-embedding-005)
- **Image**: 1408D (Vertex AI multimodalembedding@001)
- **Structured**: 3D (Z-score normalized features)
- **Combined**: 2179D (ARRAY_CONCAT integration)

### ORI Algorithm
The ORI (Discrepancy Index) algorithm combines:
- **Semantic Distance**: Cosine similarity between embeddings (weight: 0.7)
- **Rule-based Score**: Keyword matching for discrepancy terms (weight: 0.3)
- **Weighted Combination**: `ORI = w * semantic_distance + (1-w) * rule_score`

## Technical Implementation

### Database Schema
- `raw_texts`: Source text data with content hashing
- `emb_view_t_vertex`: Vertex AI text embeddings (768D)
- `emb_view_i_real`: Vertex AI image embeddings (1408D)
- `feat_struct_vec`: Structured feature vectors (3D)
- `emb_stitched_real`: Multimodal combined embeddings (2179D)
- `report_ori`: ORI analysis results
- `eval_metrics`: Performance evaluation metrics

### Performance Characteristics
- **Processing Speed**: 1.22 seconds per case
- **Recall**: 100% on labeled mismatches
- **Cost Efficiency**: $0.018 per 10k items
- **Scalability**: Incremental processing with hash-based idempotency

### Production Features
- **Error Handling**: Comprehensive retry logic and dry-run mode
- **Monitoring**: Cost tracking and performance metrics
- **Automation**: CLI interface with Makefile integration
- **Testing**: Integration tests and validation harness

## Security & Compliance

### Data Protection
- No sensitive data stored in repository
- Environment variables for configuration
- Git ignore patterns for security files
- CC BY 4.0 license for commercial use

### Best Practices
- Hash-based idempotency for incremental processing
- Partitioned and clustered tables for performance
- Externalized configuration management
- Comprehensive documentation and testing

---

**Descent AI Architecture**: Production-ready multimodal discrepancy detection powered by BigQuery AI functions.