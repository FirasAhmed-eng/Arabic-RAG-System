# Arabic RAG System

A simple Retrieval-Augmented Generation (RAG) application built with LangChain, Qdrant, and an LLM. The system extracts text from a PDF document, stores document embeddings in Qdrant, retrieves relevant chunks based on a user query, and generates context-aware answers.

## Features

* PDF document ingestion
* Text chunking
* Vector embeddings generation
* Qdrant vector database integration
* Similarity search retrieval
* Context-aware answer generation using an LLM
* Arabic language support

## Project Structure

```text
.
├── data/
│   └── SDAIA.pdf
├── ingest.py
├── chunking.py
├── vector.py
├── llm.py
├── rag.py
├── debug_output.txt
└── README.md
```

## RAG Pipeline

```text
User Query
     ↓
Embed Query
     ↓
Retrieve Top Chunks
     ↓
Build Context
     ↓
Send Context to LLM
     ↓
Generate Answer
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Arabic-RAG-System
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

Create a `.env` file and add:

```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Ingest Documents

Run the ingestion process once to create the vector store:

```bash
python ingest.py
```

This will:

* Extract text from the PDF
* Split text into chunks
* Generate embeddings
* Store vectors in Qdrant

## Run Retrieval

Execute the RAG pipeline:

```bash
python rag.py
```

The system will:

1. Receive a query
2. Retrieve the most relevant document chunks
3. Build context
4. Generate an answer using the LLM

## Example Query

```python
query = "تاريخ الذكاء الاصطناعي"
```

## Technologies Used

* Python
* LangChain
* Qdrant
* OpenAI Embeddings
* OpenAI LLM
* PDF Processing Libraries

## Future Improvements

* Interactive CLI chatbot
* Streamlit web interface
* Conversational memory
* Hybrid search (keyword + vector)
* Metadata filtering
* Multi-document support

## License

This project is intended for educational and learning purposes.
