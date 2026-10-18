import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from config import settings
from rag_engine import build_rag_chain, initialize_vectorstore, load_source_documents

# --- Page Config ---
st.set_page_config(page_title="rag-raw Assistant", page_icon="🤖", layout="wide")

st.title("💬 rag-raw: Document & URL Chat Assistant")
st.markdown(
    "Query securely against uploaded internal documents or live web URLs using conversational AI."
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=settings.OPENAI_API_KEY,
        help="Provide your active OpenAI Key.",
    )
    if api_key_input:
        settings.OPENAI_API_KEY = api_key_input

    st.markdown("---")
    st.subheader("📁 Ingestion Source")
    source_type = st.radio("Choose source type:", ["File Upload", "HTTP URL"])

    uploaded_file = None
    url_input = ""
    process_btn = False

    if source_type == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "txt", "docx"],
            help="Supported formats: PDF, TXT, DOCX",
        )
        process_btn = st.button(
            "Process File", type="primary", use_container_width=True
        )
    else:
        url_input = st.text_input("Web Link", placeholder="https://example.com/docs")
        process_btn = st.button(
            "OK / Load URL", type="primary", use_container_width=True
        )

    # --- Chunking & System Stats ---
    st.markdown("---")
    st.subheader("📊 Chunking & Status")

    if "chunk_info" in st.session_state and st.session_state.chunk_info:
        info = st.session_state.chunk_info
        st.success("Status: Vector Store Online 🟢")
        st.metric(label="Total Chunks Created", value=info["total_chunks"])
        with st.expander("View Chunk Parameters"):
            st.write(f"**Chunk Size:** {info['chunk_size']} chars")
            st.write(f"**Chunk Overlap:** {info['chunk_overlap']} chars")
            st.write(f"**Source Pages/Docs:** {info['total_docs']}")
    else:
        st.warning("Status: Awaiting Source 🟠")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "chunk_info" not in st.session_state:
    st.session_state.chunk_info = None

# --- Ingestion Process Action ---
if process_btn:
    if not settings.OPENAI_API_KEY:
        st.error("⚠️ OpenAI API Key required.")
    elif source_type == "File Upload" and not uploaded_file:
        st.warning("⚠️ Please select a file first.")
    elif source_type == "HTTP URL" and not url_input.strip():
        st.warning("⚠️ Please enter a valid URL.")
    else:
        with st.spinner("🔄 Parsing content and calculating embeddings..."):
            try:
                raw_docs = load_source_documents(uploaded_file, url_input, source_type)
                if raw_docs:
                    vstore, chunk_metadata = initialize_vectorstore(raw_docs)
                    st.session_state.rag_chain = build_rag_chain(vstore)
                    st.session_state.chunk_info = chunk_metadata
                    st.session_state.chat_history = []  # Reset thread
                    st.success("Indexing complete!")
                    st.rerun()
                else:
                    st.error("Could not extract content from source.")
            except Exception as e:  # noqa: BLE001 - never surface tracebacks in the UI
                st.error(f"Error processing source: {e}")

# --- Chat Interface ---
if not st.session_state.chat_history:
    st.info(
        "👋 Index a document or click **OK / Load URL** in the sidebar to start asking questions."
    )

for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# --- User Query Input ---
user_query = st.chat_input("Ask a question about your source content...")

if user_query:
    if not st.session_state.rag_chain:
        st.warning("⚠️ Please index a source document or URL first.")
    else:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            try:
                response_placeholder = st.empty()

                def stream_generator():
                    for chunk in st.session_state.rag_chain.stream(
                        {
                            "input": user_query,
                            "chat_history": st.session_state.chat_history[:-1],
                        }
                    ):
                        if "answer" in chunk:
                            yield chunk["answer"]

                answer = response_placeholder.write_stream(stream_generator())
                st.session_state.chat_history.append(AIMessage(content=answer))

            except Exception as e:  # noqa: BLE001 - never surface tracebacks in the UI
                st.error(f"Generation error: {e}")
