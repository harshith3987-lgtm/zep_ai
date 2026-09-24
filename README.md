
# Zepto Data & AI Platform

An end-to-end quick-commerce data and AI platform combining **web data extraction, relational data engineering, machine learning analytics, and a grounded AI support assistant**.

The repository is organized into three independent but complementary modules:

1. **`data_pipeline/`** — Catalog scraping, data cleaning, normalization, schema validation, and SQLite ingestion.
2. **`analytics/`** — Exploratory data analysis, preprocessing, feature engineering, machine learning, model evaluation, tuning, and model serialization.
3. **`support_assistant/`** — Grounded policy-question answering using local embeddings, ChromaDB, LangGraph, FastAPI, and Streamlit.

The complete platform is designed to run locally using open-source Python libraries.

---

# 1. Project Overview

## Objective

The objective of this project is to build a complete data and AI workflow for a quick-commerce platform.

The system demonstrates three major stages of an applied data/AI lifecycle:

```text
                    ZEpto Data & AI Platform
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Data Pipeline      Analytics       Support Assistant
             │                │                │
             ▼                ▼                ▼
       Web Scraping       EDA + ML       RAG + Retrieval
             │                │                │
             ▼                ▼                ▼
       SQLite Database    ML Models      ChromaDB
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    End-to-End Platform
````

---

# 2. Repository Structure

```text
Capstone_masai/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data_pipeline/
│   ├── scraper.py
│   ├── clean_and_load.py
│   ├── schema.sql
│   ├── README.md
│   └── data/
│       ├── *.json
│       └── zepto_catalog.db
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── README.md
│   └── model_artifacts/
│       └── *.joblib
│
└── support_assistant/
    ├── api.py
    ├── app.py
    ├── Dockerfile
    ├── graph.py
    ├── ingest.py
    ├── prompts.py
    ├── state.py
    ├── README.md
    ├── chroma_db/
    ├── docs/
    │   ├── doc1.txt
    │   ├── doc2.txt
    │   ├── doc3.txt
    │   ├── doc4.txt
    │   ├── doc5.txt
    │   ├── doc6.txt
    │   ├── doc7.txt
    │   └── doc8.txt
    └── .streamlit/
        └── config.toml
```

---

# 3. Technology Stack

| Area                 | Technology            | Purpose                         |
| -------------------- | --------------------- | ------------------------------- |
| Language             | Python 3.10+          | Application development         |
| Web Scraping         | Requests              | HTTP requests                   |
| Web Parsing          | BeautifulSoup4        | HTML parsing                    |
| XML/HTML Parser      | lxml                  | Structured parsing              |
| Data Processing      | NumPy                 | Numerical operations            |
| Data Processing      | Pandas                | Data manipulation               |
| Scientific Computing | SciPy                 | Scientific operations           |
| Visualization        | Matplotlib            | Data visualization              |
| Visualization        | Seaborn               | Statistical visualization       |
| Machine Learning     | Scikit-learn          | ML pipelines and models         |
| Model Persistence    | Joblib                | Saving trained models           |
| Database             | SQLite                | Relational storage              |
| LLM Framework        | LangChain             | LLM/RAG ecosystem support       |
| Workflow             | LangGraph             | Agent/workflow orchestration    |
| Vector Database      | ChromaDB              | Embedding storage and retrieval |
| Embeddings           | Sentence Transformers | Local semantic embeddings       |
| API                  | FastAPI               | REST API                        |
| Server               | Uvicorn               | ASGI server                     |
| Frontend             | Streamlit             | Interactive UI                  |
| Validation           | Pydantic              | Request/response schemas        |
| Version Control      | Git                   | Source control                  |

---

# 4. Environment Setup

## Prerequisites

Install:

* Python 3.10 or higher
* Git
* VS Code or another Python IDE

Verify Python:

```bash
python --version
```

Verify Git:

```bash
git --version
```

---

## Create Virtual Environment

From the repository root:

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source venv/bin/activate
```

After activation, the terminal should show:

```text
(venv)
```

---

## Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

# 5. Module 1 — Data Pipeline

## 5.1 Purpose

The `data_pipeline` module is responsible for converting raw web-based catalog information into structured, normalized relational data.

The pipeline follows:

```text
Web Source
    │
    ▼
Scraping
    │
    ▼
Raw JSON/Data
    │
    ▼
Cleaning & Normalization
    │
    ▼
Schema Validation
    │
    ▼
SQLite Database
```

The module demonstrates the complete process from data acquisition to structured database storage.

---

## 5.2 Module Structure

```text
data_pipeline/
│
├── scraper.py
├── clean_and_load.py
├── schema.sql
├── README.md
└── data/
    ├── extracted JSON files
    └── zepto_catalog.db
```

---

## 5.3 `scraper.py`

The `scraper.py` file is responsible for extracting catalog information from the target web source.

The general workflow is:

```text
Target Website
      │
      ▼
HTTP Request
      │
      ▼
HTML Response
      │
      ▼
HTML Parsing
      │
      ▼
Product Information
      │
      ▼
Raw Structured Data
```

The scraper uses:

* `requests`
* `BeautifulSoup`
* `lxml`

The extracted information is stored in the module's `data/` directory.

---

## 5.4 Data Extraction

The scraper converts unstructured web content into structured records.

Typical processing stages include:

```text
Request Page
     ↓
Parse HTML
     ↓
Locate Product Information
     ↓
Extract Relevant Fields
     ↓
Create Structured Records
     ↓
Save Raw Data
```

The raw extracted data is retained before database loading so that the extraction and transformation stages remain separate.

---

## 5.5 `clean_and_load.py`

The `clean_and_load.py` script is responsible for transforming extracted data into a consistent database-ready format.

The workflow is:

```text
Raw Extracted Data
       │
       ▼
Load Data
       │
       ▼
Clean Missing/Invalid Values
       │
       ▼
Normalize Fields
       │
       ▼
Normalize Units
       │
       ▼
Apply Schema Rules
       │
       ▼
Insert into SQLite
```

The cleaning stage ensures that the data conforms to the expected database structure before insertion.

---

## 5.6 Data Normalization

The pipeline normalizes heterogeneous product attributes before database insertion.

Where applicable, values such as volume and weight are converted into consistent base units.

This avoids storing equivalent measurements in multiple formats.

For example:

```text
Different Input Units
        │
        ▼
Standardized Unit
        │
        ▼
Database Storage
```

This improves consistency and makes downstream querying easier.

---

## 5.7 `schema.sql`

The `schema.sql` file defines the relational database structure.

The schema is responsible for:

* Table definitions
* Primary keys
* Foreign keys
* Data types
* Relationships
* Structural constraints

The database follows a normalized relational design.

The schema is applied before inserting cleaned records.

---

## 5.8 SQLite Database

The final relational database is stored under:

```text
data_pipeline/data/zepto_catalog.db
```

SQLite provides a lightweight local database suitable for development, analysis, and SQL querying without requiring a separate database server.

---

## 5.9 Module 1 Execution

From the repository root:

```powershell
cd data_pipeline
python scraper.py
python clean_and_load.py
cd ..
```

Expected workflow:

```text
Scrape
  ↓
Raw Data
  ↓
Clean
  ↓
Normalize
  ↓
Validate
  ↓
SQLite Database
```

---

## 5.10 Module 1 Output

The primary output is:

```text
data_pipeline/data/zepto_catalog.db
```

The module also retains extracted data files for traceability and reproducibility.

---

# 6. Module 2 — Analytics & Predictive Modeling

## 6.1 Purpose

The `analytics` module demonstrates a complete machine-learning workflow starting from dataset exploration and ending with trained model artifacts.

The workflow is:

```text
Dataset
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Data Cleaning
   │
   ▼
Feature Engineering
   │
   ▼
Encoding + Scaling
   │
   ▼
Train/Test Split
   │
   ▼
ML Pipeline
   │
   ▼
Baseline Models
   │
   ▼
Hyperparameter Tuning
   │
   ▼
Evaluation
   │
   ▼
Best Model
   │
   ▼
Joblib Artifact
```

---

## 6.2 Module Structure

```text
analytics/
│
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── README.md
└── model_artifacts/
    └── *.joblib
```

---

# 7. Exploratory Data Analysis

## 7.1 `01_eda.ipynb`

The first notebook performs exploratory data analysis.

The EDA workflow includes:

```text
Dataset Loading
      ↓
Dataset Inspection
      ↓
Data Types
      ↓
Missing Values
      ↓
Descriptive Statistics
      ↓
Correlation Analysis
      ↓
Outlier Analysis
      ↓
Feature Understanding
```

---

## 7.2 Dataset Inspection

Initial inspection identifies:

* Number of rows
* Number of columns
* Feature types
* Target variable
* Missing values
* Numerical features
* Categorical features

Typical Pandas operations include:

```python
df.head()
df.info()
df.describe()
df.isnull().sum()
```

---

## 7.3 Missing Value Analysis

Missing values are identified before model training.

The analysis determines:

```text
Column
   ↓
Missing Count
   ↓
Missing Percentage
   ↓
Treatment Strategy
```

Appropriate preprocessing is then incorporated into the machine-learning pipeline rather than manually applying transformations before cross-validation.

---

## 7.4 Statistical Analysis

Descriptive statistics are used to understand the distribution of numerical variables.

The analysis considers:

* Mean
* Median
* Standard deviation
* Minimum
* Maximum
* Quartiles

This provides an initial understanding of the dataset before modelling.

---

## 7.5 Correlation Analysis

Correlation analysis is used to understand relationships between numerical variables.

Visualizations can be generated using:

* Matplotlib
* Seaborn

The analysis helps identify potentially related features and possible multicollinearity.

---

## 7.6 Outlier Analysis

Outlier detection is performed to identify unusually large or small observations.

The analysis can use:

* Distribution plots
* Box plots
* Statistical measures

Outlier observations are examined before deciding how they should be handled.

---

# 8. Machine Learning Modeling

## 8.1 `02_modeling.ipynb`

The second notebook contains the predictive modelling workflow.

The workflow is:

```text
Load Dataset
      ↓
Separate Features and Target
      ↓
Train/Test Split
      ↓
Preprocessing Pipeline
      ↓
Baseline Models
      ↓
Model Evaluation
      ↓
Hyperparameter Tuning
      ↓
Final Evaluation
      ↓
Model Serialization
```

---

## 8.2 Data Preprocessing

Preprocessing is performed inside Scikit-learn pipelines.

This prevents preprocessing information from leaking from validation/test data into training data.

The preprocessing workflow includes:

```text
Numerical Features
      │
      ▼
Missing Value Handling
      │
      ▼
Standard Scaling
```

and:

```text
Categorical Features
      │
      ▼
Missing Value Handling
      │
      ▼
Categorical Encoding
```

Depending on the feature type, encoding can include:

* Label encoding
* One-hot encoding

---

## 8.3 Feature Scaling

Standard scaling is used where appropriate.

The purpose of scaling is to place numerical features on a comparable scale.

The transformation is performed within the ML pipeline so that the scaler is fitted only on the appropriate training data during validation.

---

## 8.4 Baseline Modeling

Baseline models are trained before tuning.

The baseline stage establishes an initial reference point for model performance.

The process is:

```text
Preprocessed Data
       ↓
Baseline Model
       ↓
Validation
       ↓
Performance Metrics
```

---

## 8.5 Model Evaluation

The appropriate evaluation metrics are selected according to the machine-learning task.

For classification, metrics may include:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

For regression, metrics may include:

* MAE
* MSE
* RMSE
* R² score

The model evaluation should consider more than a single metric where appropriate.

---

## 8.6 Cross-Validation

Cross-validation is used to provide a more reliable estimate of model performance.

The process is:

```text
Training Data
      │
      ▼
Multiple Validation Folds
      │
      ▼
Train Model
      │
      ▼
Evaluate
      │
      ▼
Compare Fold Scores
      │
      ▼
Average Performance
```

Preprocessing remains inside the pipeline to reduce data leakage.

---

## 8.7 Hyperparameter Tuning

After baseline evaluation, model hyperparameters can be optimized.

The tuning workflow is:

```text
Baseline Model
      ↓
Define Parameter Search
      ↓
Cross-Validation
      ↓
Evaluate Configurations
      ↓
Select Best Configuration
      ↓
Final Model
```

This allows the model configuration to be selected systematically rather than manually.

---

## 8.8 Model Serialization

The selected model pipeline is saved using Joblib.

```text
analytics/
└── model_artifacts/
    └── *.joblib
```

The saved artifact contains the trained machine-learning pipeline so that the same preprocessing and model configuration can be reused later.

---

## 8.9 Module 2 Execution

From the repository root:

```powershell
cd analytics
jupyter notebook
```

Run:

```text
01_eda.ipynb
```

first.

Then run:

```text
02_modeling.ipynb
```

The recommended order is:

```text
01_eda.ipynb
      ↓
02_modeling.ipynb
      ↓
model_artifacts/
```

---

# 9. Module 3 — Grounded Support Assistant

## 9.1 Purpose

The `support_assistant` module provides a grounded customer-support assistant using the supplied Zepto policy documents.

The system combines:

* Local embeddings
* ChromaDB
* LangGraph
* FastAPI
* Pydantic
* Streamlit

The baseline is deterministic and does not require an external LLM API.

---

## 9.2 Module Structure

```text
support_assistant/
│
├── docs/
│   ├── doc1.txt
│   ├── doc2.txt
│   ├── doc3.txt
│   ├── doc4.txt
│   ├── doc5.txt
│   ├── doc6.txt
│   ├── doc7.txt
│   └── doc8.txt
│
├── chroma_db/
│
├── .streamlit/
│   └── config.toml
│
├── ingest.py
├── prompts.py
├── state.py
├── graph.py
├── api.py
├── app.py
├── Dockerfile
└── README.md
```

---

# 10. Support Assistant Knowledge Base

The system contains exactly eight policy documents.

| File       | Policy                   |
| ---------- | ------------------------ |
| `doc1.txt` | Delivery Policy          |
| `doc2.txt` | Returns & Refunds        |
| `doc3.txt` | Membership Tiers         |
| `doc4.txt` | Order Tracking           |
| `doc5.txt` | Order Cancellation       |
| `doc6.txt` | Damaged or Missing Items |
| `doc7.txt` | Gift Cards               |
| `doc8.txt` | Customer Support Hours   |

These documents form the knowledge base used by the retrieval system.

---

# 11. Support Assistant Ingestion

The ingestion pipeline is implemented in:

```text
ingest.py
```

The process is:

```text
Policy Documents
      ↓
Read Documents
      ↓
Create Document IDs
      ↓
Generate Embeddings
      ↓
Normalize Embeddings
      ↓
Store in ChromaDB
```

The embedding model is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

ChromaDB stores the embeddings in:

```text
support_assistant/chroma_db/
```

The vector collection uses cosine similarity.

---

# 12. Prompt Design

The structured prompt is stored in:

```text
prompts.py
```

The prompt contains:

* Role
* Context
* Task
* Format
* Length
* Negative grounding constraint
* Few-shot example

The grounding rule ensures that responses should not use information outside the supplied context.

The current baseline does not make an external LLM call.

---

# 13. LangGraph Workflow

The workflow is implemented in:

```text
graph.py
```

The graph contains three primary nodes:

```text
classify_intent
       │
       ├───────────────┐
       │               │
       ▼               ▼
retrieve_and_answer  direct_answer
       │               │
       └───────┬───────┘
               ▼
              END
```

---

## 13.1 Intent Classification

The `classify_intent` node uses a deterministic keyword-based classifier.

Policy keywords include:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

Matching queries are routed to:

```text
policy_question
```

Other queries are routed to:

```text
general_question
```

---

## 13.2 Retrieval and Answer Generation

Policy questions are passed to:

```text
retrieve_and_answer
```

The process is:

```text
User Query
     ↓
Query Embedding
     ↓
all-MiniLM-L6-v2
     ↓
ChromaDB
     ↓
Top-3 Retrieval
     ↓
Top Retrieved Context
     ↓
Deterministic Response
```

The top three retrieved document IDs are returned as sources.

---

## 13.3 General Questions

General questions are handled by:

```text
direct_answer
```

The deterministic response is:

```text
I can only answer questions about Zepto policies right now.
```

No policy retrieval is required for this route.

---

# 14. LangGraph State

The state definition is stored in:

```text
state.py
```

The state contains:

```text
query
intent
context
answer
sources
confidence
```

This state is passed between the LangGraph nodes.

---

# 15. FastAPI Backend

The API is implemented in:

```text
api.py
```

Endpoint:

```text
POST /ask
```

Request:

```json
{
  "query": "What is the delivery time?"
}
```

Response:

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc1",
    "doc2",
    "doc4"
  ],
  "confidence": 1.0
}
```

The response schema contains:

| Field        | Type         | Purpose                    |
| ------------ | ------------ | -------------------------- |
| `answer`     | string       | Assistant response         |
| `sources`    | list[string] | Retrieved document IDs     |
| `confidence` | float        | Confidence between 0 and 1 |

---

# 16. Streamlit Frontend

The Streamlit frontend is implemented in:

```text
app.py
```

It provides:

```text
Question Input
      ↓
Submit
      ↓
FastAPI POST /ask
      ↓
Response
      ↓
Answer
Sources
Confidence
```

The frontend runs on the default Streamlit port:

```text
http://localhost:8501
```

The FastAPI backend runs on:

```text
http://127.0.0.1:7860
```

---

# 17. Module 3 Execution

From the repository root:

```powershell
cd support_assistant
```

First create or refresh the vector database:

```powershell
python ingest.py
```

Expected output:

```text
Loaded 8 documents.
Created 8 embeddings.
Stored 8 documents in ChromaDB.
Ingestion completed successfully.
```

Start FastAPI:

```powershell
uvicorn api:app --host 0.0.0.0 --port 7860
```

Swagger documentation:

```text
http://127.0.0.1:7860/docs
```

Open another terminal and start Streamlit:

```powershell
cd support_assistant
streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

# 18. Example Support Assistant Queries

## Policy Query

```json
{
  "query": "What is the delivery time?"
}
```

Example response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard del",
  "sources": [
    "doc1",
    "doc2",
    "doc4"
  ],
  "confidence": 1
}
```

## General Query

```json
{
  "query": "What is the capital of India?"
}
```

Example response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}
```

---

# 19. End-to-End Data & AI Flow

The three modules can be viewed as three independent stages of an applied data and AI platform.

```text
                     WEB / DATA SOURCES
                            │
                            ▼
                 ┌─────────────────────┐
                 │    MODULE 1          │
                 │    DATA PIPELINE     │
                 │                     │
                 │ Scraping             │
                 │ Cleaning             │
                 │ Normalization        │
                 │ SQL Schema            │
                 │ SQLite               │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    MODULE 2          │
                 │    ANALYTICS         │
                 │                     │
                 │ EDA                  │
                 │ Preprocessing        │
                 │ Feature Engineering  │
                 │ ML Training          │
                 │ Evaluation           │
                 │ Tuning               │
                 │ Model Artifacts      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    MODULE 3          │
                 │ SUPPORT ASSISTANT    │
                 │                     │
                 │ Policy Documents     │
                 │ Embeddings           │
                 │ ChromaDB             │
                 │ LangGraph            │
                 │ FastAPI              │
                 │ Streamlit            │
                 └─────────────────────┘
```

---

# 20. Data Engineering Design

The data engineering component focuses on transforming raw external information into structured and usable data.

```text
Raw Web Data
     ↓
Extraction
     ↓
Cleaning
     ↓
Normalization
     ↓
Schema Validation
     ↓
Relational Storage
```

Key design principles:

* Separate extraction from transformation.
* Preserve raw extracted data.
* Normalize inconsistent units.
* Apply database constraints.
* Store structured data in SQLite.
* Keep the pipeline reproducible.

---

# 21. Machine Learning Design

The analytics component follows a leakage-aware machine-learning workflow.

```text
Raw Dataset
     ↓
EDA
     ↓
Feature Identification
     ↓
Train/Test Split
     ↓
Preprocessing Pipeline
     ↓
Model Training
     ↓
Cross-Validation
     ↓
Hyperparameter Tuning
     ↓
Evaluation
     ↓
Serialized Model
```

Important preprocessing operations are maintained inside Scikit-learn pipelines.

This keeps transformations consistent between training and evaluation.

---

# 22. RAG Design

The support assistant follows a retrieval-grounded architecture.

```text
                 KNOWLEDGE BASE
                      │
                      ▼
              Document Ingestion
                      │
                      ▼
                 Embeddings
                      │
                      ▼
                  ChromaDB
                      │
                      │
User Query ───────────┘
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Top-3 Documents
      │
      ▼
Grounded Answer
```

The system does not rely on unrestricted external knowledge for the deterministic baseline.

---

# 23. Reproducibility

The project is designed to be reproducible using:

* A Python virtual environment
* A consolidated `requirements.txt`
* Local datasets/documents
* Local SQLite storage
* Local ChromaDB storage
* Serialized model artifacts
* Git version control

The main setup process is:

```bash
python -m venv venv
```

```bash
pip install -r requirements.txt
```

Then each module can be executed independently.

---

# 24. Consolidated Dependencies

The root `requirements.txt` contains the major dependencies required across the project.

```text
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0

numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0

matplotlib>=3.7.0
seaborn>=0.12.0

scikit-learn>=1.3.0
joblib>=1.3.0

langchain>=0.1.0
langchain-community>=0.0.20
langchain-core>=0.1.20

chromadb>=0.4.22
sentence-transformers>=2.2.2

fastapi
uvicorn
streamlit
langgraph
pydantic
```

---

# 25. Module-wise Quick Start

## Module 1

```powershell
cd data_pipeline
python scraper.py
python clean_and_load.py
```

Output:

```text
data_pipeline/data/zepto_catalog.db
```

---

## Module 2

```powershell
cd analytics
jupyter notebook
```

Run:

```text
01_eda.ipynb
02_modeling.ipynb
```

Output:

```text
analytics/model_artifacts/
```

---

## Module 3

```powershell
cd support_assistant
python ingest.py
uvicorn api:app --host 0.0.0.0 --port 7860
```

In another terminal:

```powershell
cd support_assistant
streamlit run app.py
```

---

# 26. Project Outputs

The major outputs of the project are:

### Module 1

```text
Raw catalog data
       ↓
Cleaned data
       ↓
SQLite database
```

### Module 2

```text
EDA results
       ↓
Model evaluation
       ↓
Best ML pipeline
       ↓
.joblib model artifact
```

### Module 3

```text
Policy documents
       ↓
Embeddings
       ↓
ChromaDB
       ↓
Grounded responses
       ↓
FastAPI + Streamlit
```

---

# 27. Current Implementation Status

| Module   | Component             | Status      |
| -------- | --------------------- | ----------- |
| Module 1 | Web scraping          | Implemented |
| Module 1 | Data cleaning         | Implemented |
| Module 1 | Normalization         | Implemented |
| Module 1 | SQL schema            | Implemented |
| Module 1 | SQLite ingestion      | Implemented |
| Module 2 | EDA                   | Implemented |
| Module 2 | Preprocessing         | Implemented |
| Module 2 | ML pipelines          | Implemented |
| Module 2 | Model evaluation      | Implemented |
| Module 2 | Hyperparameter tuning | Implemented |
| Module 2 | Model serialization   | Implemented |
| Module 3 | Policy corpus         | Implemented |
| Module 3 | Embedding ingestion   | Implemented |
| Module 3 | ChromaDB retrieval    | Implemented |
| Module 3 | LangGraph workflow    | Implemented |
| Module 3 | FastAPI               | Implemented |
| Module 3 | Streamlit UI          | Implemented |
| Module 3 | Dockerfile            | Added       |

---

# 28. Limitations

The current implementation has several deliberate limitations.

### Data Pipeline

The scraping pipeline depends on the availability and structure of the target web source. Changes to the website structure may require scraper updates.

### Analytics

Model performance depends on the supplied dataset, preprocessing decisions, selected algorithms, and available features.

### Support Assistant

The current support assistant uses a deterministic keyword-based intent classifier and deterministic response generation for the baseline.

The knowledge base is limited to the eight supplied policy documents.

The Docker configuration is included, but Docker execution has not been locally verified.

---

# 29. Future Improvements

Potential improvements across the platform include:

## Data Pipeline

* Automated scheduled scraping
* Incremental database updates
* Additional validation rules
* Data quality monitoring
* Larger catalog coverage

## Analytics

* Additional feature engineering
* More model comparisons
* Automated experiment tracking
* Model explainability
* Prediction API
* Model monitoring

## Support Assistant

* Improved semantic intent classification
* Optional LLM-based response generation
* Better document chunking
* Conversation history
* Source-level citations
* Retrieval evaluation
* Authentication
* Rate limiting
* Production deployment

---

# 30. Git Workflow

The project uses Git for version control.

Check repository status:

```bash
git status
```

Check branches:

```bash
git branch
```

Stage the required project files:

```bash
git add README.md requirements.txt data_pipeline analytics support_assistant
```

Create a commit:

```bash
git commit -m "Complete end-to-end Zepto data and AI platform"
```

Push changes:

```bash
git push
```

---

# 31. Final Architecture

```text
                           ZEpto DATA & AI PLATFORM
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
   ┌───────────────┐           ┌───────────────┐          ┌───────────────┐
   │   MODULE 1    │           │   MODULE 2    │          │   MODULE 3    │
   │ Data Pipeline │           │  Analytics    │          │   Support AI  │
   └───────┬───────┘           └───────┬───────┘          └───────┬───────┘
           │                           │                           │
           ▼                           ▼                           ▼
      Web Scraping                  EDA                      Policy Corpus
           │                           │                           │
           ▼                           ▼                           ▼
      Data Cleaning              Preprocessing               Embeddings
           │                           │                           │
           ▼                           ▼                           ▼
      Normalization               ML Pipelines                ChromaDB
           │                           │                           │
           ▼                           ▼                           ▼
       SQL Schema                Model Training              LangGraph
           │                           │                           │
           ▼                           ▼                           ▼
        SQLite                  Evaluation/Tuning            FastAPI
                                       │                           │
                                       ▼                           ▼
                                  Joblib Model                Streamlit
```

---

# 32. Conclusion

The **Zepto Data & AI Platform** demonstrates an end-to-end engineering workflow covering three major areas:

1. **Data Engineering** — extracting, cleaning, normalizing, validating, and storing catalog data.
2. **Machine Learning** — exploring data, building leakage-aware preprocessing pipelines, training models, evaluating performance, tuning hyperparameters, and saving model artifacts.
3. **Applied GenAI/RAG** — embedding policy documents, performing vector retrieval, orchestrating responses through LangGraph, exposing the system through FastAPI, and providing an interactive Streamlit interface.

Together, the three modules demonstrate a complete progression:

```text
Data Acquisition
       ↓
Data Engineering
       ↓
Data Storage
       ↓
Data Analysis
       ↓
Machine Learning
       ↓
Model Artifacts
       ↓
Knowledge Retrieval
       ↓
AI Support Application
       ↓
API + User Interface
```

The repository is structured so that each module can be developed, executed, tested, and maintained independently while forming a complete end-to-end data and AI platform.
