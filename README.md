# 💬 rag-raw: Document & URL Chat Assistant

`rag-raw` is a modular, production-ready Retrieval-Augmented Generation (RAG) web application built with **Streamlit**, **LangChain**, and **OpenAI**. It allows users to securely upload documents (`PDF`, `TXT`, `DOCX`) or point to public web URLs (`HTTP URL`) and chat conversationally with the underlying content.

---

## 🚀 Key Features

* **Multi-Source Ingestion**: Upload internal files or index live web pages instantly.
* **History-Aware Conversations**: Retains full chat context so follow-up questions are accurately contextualized.
* **Real-Time Token Streaming**: Responses stream onto the UI gracefully.
* **Chunking Metrics Dashboard**: Displays real-time metrics for total vector chunks, chunk size, overlap, and source count.
* **Modern Tooling**: Built with **`uv`** for lightning-fast package management, **`ruff`** for linting, and **`pytest`** for unit testing.

---

## 📁 Project Structure

```text
rag-raw/
├── .env                  # Environment variables (OpenAI API key, settings)
├── .env.example          # Template for environment configuration
├── .gitignore            # Git ignore file
├── pyproject.toml        # Project dependencies, uv, ruff, and pytest config
├── config.py             # Configuration & environment settings management
├── llm_client.py         # Isolated OpenAI LLM & Embeddings initialization
├── rag_engine.py         # Document parsing, chunking, vector store, & RAG chain
├── app.py                # Main Streamlit user interface & session state
└── tests/
    └── test_config.py    # Unit test suite
```

## 🛠️ Prerequisites & Installation

Make sure you have [uv](https://docs.astral.sh/uv/) installed on your system.

Clone the repository and enter the directory:

```bash
cd rag-raw
```

Sync dependencies using `uv`:

```bash
uv sync
```

Configure your environment variables.
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY="sk-your-actual-api-key-here"
MODEL_NAME="gpt-4o-mini"
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## 🏃 Running the Application

Launch the Streamlit user interface:

```bash
uv run streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501) to start interacting with the app.

## 🧪 Testing & Code Quality

Run Unit Tests (`pytest`):

```bash
uv run pytest
```

Run Linting & Formatting Checks (`ruff`):

```bash
uv run ruff check .
```
