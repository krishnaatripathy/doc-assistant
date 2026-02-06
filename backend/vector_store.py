import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "data/vector_index.faiss"
META_PATH = "data/chunk_metadata.pkl"

def build_faiss_index(embeddings, metadata):
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    return index

def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
