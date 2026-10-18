# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Browser-like `User-Agent` and request timeout for URL ingestion.
- Guards for unsupported file formats and empty/unreadable sources.
- `python-docx`-based `.docx` text extraction, including tables.
- README and CHANGELOG documentation.

### Changed

- Migrated chain imports from `langchain.chains` to `langchain_classic.chains` for LangChain 1.x compatibility.
- `get_llm()` now omits `temperature` for models that only accept the default (e.g. `gpt-5*`, `gpt-6*`, `o1*`, `o3*`, `o4*`, `codex*`).
- URL input is normalized to `https://` when no scheme is provided.
- Ingestion and chat handlers now surface clean error messages instead of raw tracebacks.

### Fixed

- `.docx` uploads no longer fail with `ImportError: unstructured package not found`.
- Chat generation no longer fails with HTTP 400 when using a model that rejects a non-default temperature.

## [0.1.0] - 2026-10-17

### Added

- Streamlit chat UI with sidebar configuration and API key input.
- Multi-source ingestion: `PDF`, `TXT`, `DOCX` uploads and `HTTP URL` web pages.
- FAISS vector store built from `RecursiveCharacterTextSplitter` chunks.
- History-aware conversational RAG chain with streaming responses.
- Chunking metrics dashboard (total chunks, chunk size, overlap, source count).
- Project tooling with `uv`, `ruff`, and `pytest`.

[Unreleased]: https://example.com/rag-raw/compare/v0.1.0...HEAD
[0.1.0]: https://example.com/rag-raw/releases/tag/v0.1.0
