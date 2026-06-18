# Arabic RAG System

An Arabic Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, Qdrant, OpenAI, and Next.js.

The system allows users to upload Arabic PDF documents, automatically extract and chunk their content, generate embeddings, store vectors in Qdrant, retrieve relevant context, and generate grounded answers using an LLM.

---

## Features

* Arabic PDF ingestion
* Recursive text chunking
* OpenAI embeddings
* Qdrant vector database
* Semantic similarity search
* Context-aware answer generation
* FastAPI backend
* Next.js frontend
* RAG evaluation with Ragas
* Arabic language support

---

## Architecture

```text
PDF Upload
     │
     ▼
Text Extraction
     │
     ▼
Chunking
     │
     ▼
Embedding Generation
     │
     ▼
Qdrant Vector Store
     │
     ▼
User Query
     │
     ▼
Similarity Search
     │
     ▼
Context Construction
     │
     ▼
LLM Generation
     │
     ▼
Answer
```

---

## Project Structure

```text
Arabic-RAG-System/
│
├── backend/
│   ├── api/
│   │   └── main.py
│   │
│   └── rag/
│       ├── chunking.py
│       ├── ingest.py
│       ├── llm.py
│       ├── rag.py
│       ├── vector.py
│       └── eval_ragas.py
│
├── frontend/
│   └── Next.js application
│
├── data/
│
├── requirements.txt
└── README.md
```

---

## Tech Stack

### Backend

* FastAPI
* LangChain
* OpenAI
* Qdrant
* Ragas

### Frontend

* Next.js
* React
* TypeScript

### Vector Database

* Qdrant Cloud

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Arabic-RAG-System
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key

QDRANT_ENDPOINT=your_qdrant_endpoint
QDRANT_API_KEY=your_qdrant_api_key
```

---

## Running the Backend

```bash
uvicorn backend.api.main:app --reload
```

Backend API:

```text
http://localhost:8000
```

---

## Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

## Uploading Documents

The upload endpoint:

```http
POST /api/upload
```

Workflow:

1. Save uploaded PDF
2. Extract text
3. Chunk text
4. Generate embeddings
5. Store vectors in Qdrant

---

## Asking Questions

Example:

```text
ما هو الذكاء الاصطناعي؟
```

The system:

1. Embeds the query
2. Retrieves relevant chunks
3. Builds context
4. Sends context to the LLM
5. Returns a grounded answer

---

## RAG Evaluation

The project includes Ragas evaluation.

Current metrics:

* Faithfulness

Example:

```bash
python -m backend.rag.eval_ragas
```

Evaluation workflow:

```text
Question
    ↓
Retrieve Context
    ↓
Generate Answer
    ↓
Ragas Evaluation
    ↓
Score Export
```

Results are saved to:

```text
score.csv
```

---

## Important Note About Vector Indexing

Each chunk receives a stable identifier:

```text
<source>_p<page>_c<chunk>
```

Example:

```text
SDAIAPublications09.pdf_p8_c1
```

These IDs are converted into deterministic UUIDs before insertion into Qdrant.

This prevents duplicate vectors when re-uploading the same PDF and ensures existing vectors are updated instead of duplicated.

---

## Future Improvements

* Hybrid search (BM25 + Vector Search)
* Reranking
* Multi-document collections
* Citation support
* Conversational memory
* Additional Ragas metrics
* Automated benchmark dataset generation

---

## License

This project is intended for educational and research purposes.
