from langchain_huggingface.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    print("Maintain Silence Let Me Think...")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
