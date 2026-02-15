from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import time
import threading

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

# -------- GLOBAL STATE --------
_rag_chain = None
_rag_loading = False   # prevents double loading


# -------- BACKGROUND WARMUP --------
def warm_rag_chain():
    global _rag_chain, _rag_loading

    if _rag_chain is not None or _rag_loading:
        return

    try:
        _rag_loading = True
        print("🔥 Background RAG warmup starting...")

        from main import Rag_chain
        _rag_chain = Rag_chain()

        print("✅ Background RAG warmup completed")

    except Exception as e:
        print("⚠ Background warmup failed:", e)

    finally:
        _rag_loading = False


# -------- STARTUP --------
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI app starting...")

    # Start background warmup (DOES NOT BLOCK PORT OPEN)
    threading.Thread(target=warm_rag_chain, daemon=True).start()


# -------- SAFE GETTER --------
def get_rag_chain():
    global _rag_chain, _rag_loading

    # If already ready
    if _rag_chain is not None:
        return _rag_chain

    # If not loading yet → start background load
    if not _rag_loading:
        threading.Thread(target=warm_rag_chain, daemon=True).start()

    # Wait until ready (safe wait loop)
    print("⏳ Waiting for RAG chain to be ready...")
    while _rag_chain is None:
        time.sleep(1)

    return _rag_chain


# -------- REQUEST MODEL --------
class ChatRequest(BaseModel):
    message: str


# -------- HEALTH --------
@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "rag_loaded": _rag_chain is not None,
        "rag_loading": _rag_loading
    }


# -------- ASK --------
@app.post("/ask")
def ask(request: ChatRequest):

    print("📩 Request received")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        rag = get_rag_chain()

        print("🧠 Running RAG inference...")
        start = time.time()

        answer = rag.invoke(request.message)

        print(f"✅ Answer generated in {time.time() - start:.2f}s")

        return {"answer": answer}

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Vector store not initialized. Upload docs first."
        )

    except Exception as e:
        print("❌ ASK FAILED:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -------- UPLOAD --------
@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):

    global _rag_chain

    print(f"📤 Received {len(files)} file(s)")

    documents_path = "documents/"
    os.makedirs(documents_path, exist_ok=True)

    uploaded_files = []

    try:
        from ingestion import ingest_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    for file in files:

        if not file.filename.endswith((".pdf", ".txt", ".docx")):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.filename}"
            )

        file_path = os.path.join(documents_path, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    try:
        print("🔄 Running ingestion...")
        ingest_data(documents_path)
        print("✅ Ingestion done")

        # Reset chain and rewarm in background
        _rag_chain = None
        threading.Thread(target=warm_rag_chain, daemon=True).start()

        return {
            "message": f"Processed {len(uploaded_files)} files",
            "files": uploaded_files
        }

    except Exception as e:
        print("❌ INGEST FAILED:", e)
        raise HTTPException(status_code=500, detail=str(e))
