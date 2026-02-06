from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
import numpy as np

from backend.extract_text import extract_text_from_file
from backend.chunk_text import chunk_text
from backend.generate_embeddings import generate_embedding
from backend.vector_store import build_faiss_index
from backend.rag_answer import generate_answer


app = FastAPI()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

FAISS_INDEX = None
CHUNK_METADATA = []
INDEX_READY = False

@app.get("/")
def root():
    return {"message": "Project is alive"}
#upload
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    global FAISS_INDEX, CHUNK_METADATA, INDEX_READY

    #save
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #extract
    extracted_path = extract_text_from_file(file.filename)

    #read extracted text
    with open(extracted_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted")

    #chunk text
    chunks = chunk_text(text)

    #generate embeddings
    embeddings = [generate_embedding(chunk) for chunk in chunks]

    # store metadata
    CHUNK_METADATA = [
        {"text": chunk, "source": file.filename}
        for chunk in chunks
    ]

    #build FAISS index
    FAISS_INDEX = build_faiss_index(embeddings, CHUNK_METADATA)
    INDEX_READY = True

    return {
        "message": "Document uploaded and indexed successfully",
        "chunks_indexed": len(chunks)
    }

#ask
@app.post("/ask")
def ask_question(question: str, strict: bool = True):
    if not INDEX_READY:
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    #embed question
    query_embedding = generate_embedding(question)

    #search FAISS
    D, I = FAISS_INDEX.search(
        np.array([query_embedding]).astype("float32"),
        k=3
    )

    #strict-mode refusal
    if strict and D[0][0] > 1.2:
        return {"answer": "Not found in the provided documents.", "mode": "strict"}

    #retrieve chunks
    retrieved_chunks = [CHUNK_METADATA[idx]["text"] for idx in I[0]]
    context = "\n\n".join(retrieved_chunks)

    #generate answer
    answer = generate_answer(context, question)

    return {
        "question": question,
        "answer": answer,
        "mode": "strict" if strict else "lenient",
        "sources": retrieved_chunks
    }

#summary
@app.get("/summary")
def summarize_document():
    if not INDEX_READY:
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    combined_text = "\n\n".join(
        [meta["text"] for meta in CHUNK_METADATA[:5]]
    )

    summary_prompt = (
        "Provide a concise technical summary of the following document:\n\n"
        + combined_text
    )

    summary = generate_answer(combined_text, summary_prompt)

    return {
        "summary": summary
    }


