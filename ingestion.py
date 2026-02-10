from langchain_community.document_loaders import PyPDFLoader
from splitter import get_text_splitter
from vector_store import create_faiss_from_documents
import os


# RAW_DATA_PATH = "documents/"
def load_documents(documents_path):
    docs = []
    for filename in os.listdir(documents_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(documents_path, filename))
            docs.extend(loader.load())
    return docs

def ingest_data(documents_path):
    # print("Loading documents...")
    documents = load_documents(documents_path)

    # print("Splitting documents...")
    chunks = get_text_splitter().split_documents(documents)

    # print("Loading or creating FAISS vector store...")
    vector_store = create_faiss_from_documents(chunks)
    
    # print(f"Ingestion complete! Vector store ready with {len(chunks)} chunks.")
    return vector_store


# if __name__ == "__main__":
#     ingest_data()
