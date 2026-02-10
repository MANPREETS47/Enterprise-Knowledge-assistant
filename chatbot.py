import streamlit as st
from main import Rag_chain
from ingestion import ingest_data
import os

Documents_path = "documents/"

@st.cache_resource(show_spinner=False)
def get_bot():
    return Rag_chain()


bot = get_bot()

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
                st.session_state["uploaded_files"] = uploaded_files
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(Documents_path, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                ingest_data(Documents_path)
                st.success(f"Added {len(uploaded_files)} file(s)")
                st.cache_resource.clear()
st.divider()


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

    # Get assistant answer
    with st.spinner("Thinking..."):
        answer = bot.invoke(user_input)
        with st.chat_message("assistant"):
            st.markdown(answer)
        

    # Add assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # Force clean rerun
    st.rerun()





