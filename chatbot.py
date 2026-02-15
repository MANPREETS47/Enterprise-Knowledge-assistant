import streamlit as st
import httpx
from ingestion import ingest_data
import os
import requests

Documents_path = "documents/"
API_URL = "https://enterprise-knowledge-assistant-5.onrender.com" or "http://localhost:8000"# FastAPI server URL

def ask_api_stream(question: str):
    """Stream response from FastAPI backend token by token (generator)."""
    try:
        with requests.post(
            f"{API_URL}/ask/stream",
            json={"message": question},
            stream=True,
            timeout=180,
        ) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk
    except requests.ConnectionError:
        st.error(f"❌ Cannot connect to backend server at {API_URL}")
        st.info("👉 Make sure FastAPI is running: `uvicorn api:app --reload`")
        yield "Backend server is not running. Please start it first."
    except requests.Timeout:
        st.error("⏱️ Request timed out. The model might be taking too long.")
        yield "The request timed out. Please try again."
    except requests.HTTPError as e:
        st.error(f"API Error: {str(e)}")
        yield "Sorry, I couldn't process your question. Please try again."
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        yield "An unexpected error occurred."


def upload_files_to_api(files) -> bool:
    """Upload files to FastAPI backend for processing"""
    try:
        files_data = [("files", (file.name, file.getvalue(), file.type)) for file in files]
        response = httpx.post(
            f"{API_URL}/upload",
            files=files_data,
            timeout=120.0  # Longer timeout for document processing
        )
        response.raise_for_status()
        result = response.json()
        st.info(f"✅ {result.get('message', 'Upload successful')}")
        return True
    except httpx.ConnectError:
        st.error(f"❌ Cannot connect to backend server at {API_URL}")
        st.info("👉 Make sure FastAPI is running: `uvicorn api:app --reload`")
        return False
    except httpx.TimeoutException:
        st.error("⏱️ Upload timed out. Files might be too large or processing is slow.")
        return False
    except httpx.HTTPStatusError as e:
        st.error(f"❌ Upload failed with status {e.response.status_code}")
        try:
            error_detail = e.response.json().get('detail', str(e))
            st.error(f"Error details: {error_detail}")
        except:
            st.error(f"Error: {str(e)}")
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error during upload: {str(e)}")
        st.exception(e)
        return False

st.set_page_config(page_title="Enterprise Knowledge Assistant", layout="wide")
st.title("🧠 Enterprise Knowledge Assistant")

# Upload control placed just above the chat input for a clean UI
with st.container():
    upload_col, _ = st.columns([1, 5])
    with upload_col:
        with st.sidebar.header("📎 Upload Documents"):
            uploaded_files = st.sidebar.file_uploader(
                "Upload document(s)",
                type=["pdf", "txt", "docx"],
                accept_multiple_files=True,
                label_visibility="collapsed",
                key="uploader",
            )
            if uploaded_files:
                # Check if these are new files (not already uploaded)
                current_file_names = set([f.name for f in uploaded_files])
                
                if current_file_names != st.session_state.uploaded_file_names:
                    # New files detected
                    new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_file_names]
                    
                    if new_files:
                        with st.spinner(f"Uploading {len(new_files)} new document(s) to backend..."):
                            if upload_files_to_api(new_files):
                                # Update session state with uploaded file names
                                st.session_state.uploaded_file_names.update([f.name for f in new_files])
                            else:
                                st.warning("⚠️ Upload failed. Please check the errors above and try again.")
st.divider()

# Initialize session state for uploaded files tracking
if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = set()

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---- HANDLE INPUT FIRST ----
if user_input := st.chat_input("Enter your question:"):

    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream assistant answer
    with st.chat_message("assistant"):
        answer = st.write_stream(ask_api_stream(user_input))

    # Add assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )





