# 🧠 Enterprise Knowledge Assistant

A powerful RAG (Retrieval-Augmented Generation) system that enables intelligent document search and question-answering using AI. Upload your documents and get accurate answers based on your knowledge base.

## ✨ Features

- **📄 Document Ingestion**: Upload and process PDF documents
- **🔍 Intelligent Retrieval**: FAISS-powered vector search for fast and accurate document retrieval
- **💬 Interactive Chatbot**: Streamlit-based user interface for natural conversations
- **🚀 REST API**: FastAPI backend for programmatic access
- **🤖 AI-Powered**: LangChain integration with support for multiple LLM providers (Google GenAI, Ollama)
- **📊 Document Chunking**: Smart text splitting for optimal retrieval performance

## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns:

```
├── chatbot.py         # Streamlit UI interface
├── api.py            # FastAPI REST endpoints
├── main.py           # RAG chain orchestration
├── ingestion.py      # Document loading and processing
├── retriever.py      # Retrieval logic
├── vector_store.py   # FAISS vector database
├── embeddings.py     # Text embedding generation
├── llm.py            # Language model configuration
├── splitter.py       # Text chunking strategies
├── prompt.py         # Prompt templates
└── format.py         # Document formatting utilities
```

## 🛠️ Tech Stack

- **LangChain**: Framework for LLM applications
- **FAISS**: Vector similarity search
- **Streamlit**: Interactive web UI
- **FastAPI**: High-performance REST API
- **Sentence Transformers**: Text embeddings
- **PyPDF**: PDF document parsing
- **Google GenAI / Ollama**: LLM providers

## 📋 Prerequisites

- Python 3.8+
- pip or uv package manager

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   # Or configure Ollama if using local models
   ```

## 💻 Usage

### Streamlit Chatbot Interface

Launch the interactive web interface:

```bash
streamlit run chatbot.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Upload documents via the sidebar
- Ask questions in natural language
- Get AI-powered answers based on your documents
- View conversation history

### FastAPI REST API

Start the API server:

```bash
uvicorn api:app --reload
```

Access the API at `http://localhost:8000`

**Endpoints:**
- `GET /health` - Health check
- `POST /ask` - Send a question and receive an answer

**Example API Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the main topic of the document?"}'
```

## 📁 Project Structure

### Core Components

- **`main.py`**: Constructs the RAG chain using LangChain's Runnable components
- **`ingestion.py`**: Handles document loading, splitting, and vector store creation
- **`retriever.py`**: Configures the retrieval logic from the vector database
- **`vector_store.py`**: Manages FAISS index creation and persistence
- **`embeddings.py`**: Provides embedding model configuration
- **`llm.py`**: Configures the language model (Google GenAI or Ollama)
- **`splitter.py`**: Implements text splitting strategies
- **`prompt.py`**: Contains prompt templates for the RAG system
- **`format.py`**: Utilities for formatting retrieved documents

### Data Directories

- **`documents/`**: Store your PDF files here
- **`data/faiss_index/`**: Persisted FAISS vector index

## 🔧 Configuration

### Modify Text Splitting

Edit [splitter.py](splitter.py) to adjust chunk size and overlap:

```python
chunk_size = 1000      # Adjust as needed
chunk_overlap = 200    # Adjust as needed
```

### Change LLM Provider

Edit [llm.py](llm.py) to switch between Google GenAI and Ollama or add new providers.

### Customize Prompts

Modify [prompt.py](prompt.py) to adjust the system behavior and response style.

## 📝 Example Workflow

1. **Upload Documents**: Place PDF files in the `documents/` folder or upload via the Streamlit UI
2. **Ingestion**: Documents are automatically processed and embedded
3. **Query**: Ask questions through the chatbot or API
4. **Retrieval**: System finds relevant document chunks
5. **Generation**: LLM generates an answer based on retrieved context

## 🐛 Troubleshooting

### Common Issues

- **Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`
- **API key errors**: Verify your `.env` file contains the correct API keys
- **FAISS index errors**: Delete `data/faiss_index/` and re-ingest documents
- **Out of memory**: Reduce chunk size or use smaller embedding models

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss)
- UI created with [Streamlit](https://streamlit.io/)

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**⭐ If you find this project helpful, please consider giving it a star!**

    

