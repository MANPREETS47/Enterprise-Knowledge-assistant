def format_docs(docs):
    context_text = "\n\n".join(doc.page_content for doc in docs)
    return context_text
