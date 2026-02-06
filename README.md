-> Doc Assistant

A local Retrieval-Augmented Generation (RAG) system for document-based Q&A.

-> Features
- Upload PDF documents
- Semantic search using FAISS
- Local embeddings with sentence-transformers
- AI-powered answers using a locally hosted LLM (Ollama)

-> Tech Stack
- Python
- Streamlit (UI)
- FastAPI (backend)
- FAISS
- Sentence Transformers
- Ollama (local LLM)

-> How to run locally
1. Install requirements:
   (bash) pip install -r requirements.txt
2. Run Ollama:
   (bash) ollama run llama3
3. Start the backend (FastAPI)
   (bash) uvicorn backend.main:app --reload
    The backend will run on:
    http://127.0.0.1:8000
4. Start the app:
   (bash)streamlit run ui/app.py
