import os
from langchain_community.vectorstores import FAISS
from embeddings import get_embedding_model

VECTOR_DB_PATH = "data/faiss_index"


def create_faiss_from_documents(docs):
    embeddings = get_embedding_model()

    if os.path.exists(VECTOR_DB_PATH):
        # print("Loading existing FAISS index...")
        db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        
        # print(f"Adding {len(docs)} new chunks to FAISS...")
        db.add_documents(docs)
        
        # print("Saving updated FAISS index...")
        db.save_local(VECTOR_DB_PATH)
        return db
    
    # print("Creating new FAISS index...")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTOR_DB_PATH)

    return db

def load_faiss():
    
    embeddings = get_embedding_model()

    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(
            "FAISS index not found. Run indexing first!"
        )

    # print("Loading FAISS index for retrieval...")
    db = FAISS.load_local(
        VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True
    )
    return db

    