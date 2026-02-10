from vector_store import load_faiss
# from langchain_community.retrievers import BM25Retriever
# from langchain.retrievers.ensemble import EnsembleRetriever
# from ingestion import load_documents


def get_retriever():
    """
    Hybrid Search Retriever: Vector (FAISS) + BM25 Keyword Search
    - Vector Search: 60% weight (semantic similarity)
    - BM25 Search: 40% weight (keyword matching)
    """
    # print("Setting up Hybrid Retriever (Vector + BM25)...")
    
    # Load FAISS vector store
    # print("Loading FAISS vector store...")
    vector_store = load_faiss()
    vector_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "lambda_mult": 0.25}
    )
    
    # # Load documents for BM25
    # print("Loading documents for BM25 retriever...")
    # documents = load_documents()
    # bm25_retriever = BM25Retriever.from_documents(documents)
    
    # # Combine both retrievers
    # ensemble_retriever = EnsembleRetriever(
    #     retrievers=[vector_retriever, bm25_retriever],
    #     weights=[0.6, 0.4]  # 60% vector, 40% BM25
    # )
    
    return vector_retriever  # Return only vector retriever for now


# if __name__ == "__main__":
#     # Test the retriever
#     retriever = get_retriever()
    
#     # test_question = "What is Metformin?"
#     # print(f"\nTesting retriever with question: '{test_question}'")
    
#     results = retriever.invoke(test_question)
    
#     print(f"\nFound {len(results)} relevant documents:\n")
#     for i, doc in enumerate(results, 1):
#         print(f"--- Result {i} ---")
#         print(f"Content: {doc.page_content[:200]}...")
#         print(f"Metadata: {doc.metadata}\n")
