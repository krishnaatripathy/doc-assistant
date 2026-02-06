# Doc Assistant

A local AI-powered system for document-based question answering.

## Features
- Upload PDF documents
- Semantic search using FAISS
- Local embeddings with sentence-transformers
- AI-powered answers using a locally hosted LLM (Ollama)

## Tech Stack
- Python
- Streamlit (UI)
- FastAPI (backend)
- FAISS
- Sentence Transformers
- Ollama (local LLM)

## How to run locally
1. Install requirements:
   -(bash) pip install -r requirements.txt
2. Run Ollama:
   -(bash) ollama run llama3
3. Start the backend (FastAPI)
   -(bash) uvicorn backend.main:app --reload
4. Start the app:
   -(bash)streamlit run ui/app.py
