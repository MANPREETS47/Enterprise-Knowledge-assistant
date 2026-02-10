from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import Rag_chain


app = FastAPI(title="RAG Chat API")

# Cache the chain globally
_rag_chain = None


def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        print("Loading RAG chain (may take 15-30 seconds)...")
        _rag_chain = Rag_chain()
        print("RAG chain loaded!")
    return _rag_chain


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    rag = get_rag_chain()
    answer = rag.invoke(request.message)
    return {"answer": answer}

