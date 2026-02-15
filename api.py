from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingestion import ingest_data
import os
import shutil
import uvicorn


app = FastAPI(title="RAG Chat API")

# CORS middleware (optional - for browser access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI app starting...")
    print(f"✅ App is ready to receive requests")

# Cache the chain globally
_rag_chain = None


def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        print("Loading RAG chain (may take 15-30 seconds)...")
        from main import Rag_chain
        _rag_chain = Rag_chain()
        print("RAG chain loaded!")
    return _rag_chain


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    """Health check endpoint that doesn't require RAG chain"""
    return {"status": "ok", "message": "API is running"}


@app.post("/ask")
def ask(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        rag = get_rag_chain()
        answer = rag.invoke(request.message)
        return {"answer": answer}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail="Vector store not initialized. Please upload documents first.")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    """Upload and process documents for ingestion"""
    print(f"📤 Received {len(files)} file(s) for upload")
    documents_path = "documents/"
    os.makedirs(documents_path, exist_ok=True)
    
    uploaded_files = []
    
    for file in files:
        print(f"Processing file: {file.filename}")
        if not file.filename.endswith((".pdf", ".txt", ".docx")):
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
        
        # Save file
        file_path = os.path.join(documents_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        uploaded_files.append(file.filename)
        print(f"✅ Saved: {file.filename}")
    
    # Re-ingest all documents and rebuild vector store
    try:
        print("🔄 Starting document ingestion...")
        ingest_data(documents_path)
        print("✅ Document ingestion complete!")
        
        # Clear the cached RAG chain so it reloads with new documents
        global _rag_chain
        _rag_chain = None
        print("🔄 RAG chain cache cleared")
        
        return {
            "message": f"Successfully uploaded and processed {len(uploaded_files)} file(s)",
            "files": uploaded_files
        }
    except Exception as e:
        print(f"❌ Error during ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")
