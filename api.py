from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import time

print("✅ API MODULE IMPORTED")

app = FastAPI(title="RAG Chat API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache the chain globally
_rag_chain = None


# -------- STARTUP --------
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI app starting...")
    print("✅ API is ready to receive requests")
    try:
        global _rag_chain
        print("🔥 Preloading RAG chain at startup...")
        from main import Rag_chain
        _rag_chain = Rag_chain()
        print("✅ RAG preloaded successfully")
    except Exception as e:
        print(f"⚠️ RAG preload failed: {e}")


# -------- RAG LOADER --------
def get_rag_chain():
    global _rag_chain

    if _rag_chain is None:
        print("⏳ STEP A: Starting RAG chain initialization...")
        start = time.time()

        try:
            from main import Rag_chain
            _rag_chain = Rag_chain()

            print(f"✅ STEP B: RAG chain loaded in {time.time() - start:.2f}s")

        except Exception as e:
            print(f"❌ RAG LOAD FAILED: {str(e)}")
            raise e

    return _rag_chain


# -------- MODELS --------
class ChatRequest(BaseModel):
    message: str


# -------- HEALTH --------
@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}


# -------- ASK --------
@app.post("/ask")
def ask(request: ChatRequest):

    print("📩 STEP 1: Request received")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        print("⏳ STEP 2: Getting RAG chain...")
        rag = get_rag_chain()

        print("⏳ STEP 3: Running rag.invoke()...")
        start = time.time()

        answer = rag.invoke(request.message)

        print(f"✅ STEP 4: Answer generated in {time.time() - start:.2f}s")

        return {"answer": answer}

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Vector store not initialized. Please upload documents first."
        )

    except Exception as e:
        print(f"❌ ASK FAILED: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# -------- UPLOAD --------
@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):

    print(f"📤 Received {len(files)} file(s) for upload")

    documents_path = "documents/"
    os.makedirs(documents_path, exist_ok=True)

    uploaded_files = []

    try:
        from ingestion import ingest_data
    except Exception as e:
        print(f"❌ INGEST IMPORT FAILED: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    for file in files:
        print(f"Processing file: {file.filename}")

        if not file.filename.endswith((".pdf", ".txt", ".docx")):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.filename}"
            )

        file_path = os.path.join(documents_path, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)
        print(f"✅ Saved: {file.filename}")

    try:
        print("🔄 Starting ingestion...")
        ingest_data(documents_path)
        print("✅ Ingestion complete")

        global _rag_chain
        _rag_chain = None
        print("🔄 RAG cache cleared")

        return {
            "message": f"Processed {len(uploaded_files)} file(s)",
            "files": uploaded_files
        }

    except Exception as e:
        print(f"❌ INGEST FAILED: {e}")
        raise HTTPException(status_code=500, detail=str(e))
