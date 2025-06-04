# Doc Chatbot

> A simple documentation‐focused chatbot service designed to help users query and navigate project documentation in natural language.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [Running the Server](#running-the-server)  
   - [Interactive API Docs](#interactive-api-docs)  
   - [Example Queries](#example-queries)  
6. [Project Structure](#project-structure)  
7. [Configuration](#configuration)  
8. [Adding New Documentation Sources](#adding-new-documentation-sources)  
9. [Troubleshooting](#troubleshooting)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## Project Overview

**Doc Chatbot** is a lightweight backend service that exposes a RESTful API allowing users to ask questions about project documentation (Markdown files, PDFs, etc.) and receive contextual answers. Under the hood, it typically:

- Loads and indexes your documentation files (e.g., Markdown, PDF)  
- Uses a simple retrieval or embedding-based approach to find relevant passages  
- Optionally leverages an LLM (e.g., OpenAI, local LLaMA, etc.) to generate human-readable answers  

This is part of the **12-Month AI Project Program** (Month 1 / Week 1), aiming to build a foundational “doc-bot” prototype.

---

## Features

- 🔍 Indexes local docs (Markdown, PDF) and builds a queryable knowledge base  
- 🗣️ Exposes a `/chat` endpoint (FastAPI) where users post questions and receive responses  
- 📑 Automatically reloads documentation when files change (watch mode)  
- 🌐 Built‐in OpenAPI UI (`/docs`) for interactive testing  
- 🧩 Easily extendable: swap out the retrieval backend (e.g., from simple keyword search to embeddings)  

---

## Prerequisites

- **macOS, Linux, or Windows**  
- **Python 3.8+** (we recommend 3.9 or 3.10)  
- (Optional) `virtualenv` or `venv` for creating an isolated environment  
- An API key if you plan to use an external LLM (e.g., OpenAI)  
- Git (to clone the repo)  

---

## Installation

1. **Clone this repository** (if you haven’t already):
   ```bash
   git clone https://github.com/Adimad01/12-month-AI-project-program-.git
   cd 12-month-AI-project-program-/
   git checkout 443cbbf54584ab56a3822b0c4756d7e1bb3a4d5f
   cd "Month 1/Week 1/ Doc Chatbot"
   ```

2. **Create and activate a Python virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   > If you don’t have a `requirements.txt`, you can manually install:
   > ```bash
   > pip install fastapi uvicorn openai python-multipart
   > ```

4. **Set up environment variables** (e.g., your OpenAI API key). In macOS/Linux, you can do:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
   On Windows (PowerShell):
   ```powershell
   setx OPENAI_API_KEY "your_api_key_here"
   ```

---

## Usage

### Running the Server

With your venv activated, start the FastAPI server via Uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- `main:app` assumes your FastAPI instance is defined as `app` in `main.py`.
- `--reload` watches your Python files and reloads on change (development mode).

Once started, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Interactive API Docs

Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser. FastAPI’s built-in Swagger UI will list all available endpoints (e.g., `/chat`) and allow you to send test requests directly.

### Example Queries

1. **Basic question**  
   ```bash
   POST http://localhost:8000/chat
   Content-Type: application/json

   {
     "question": "How do I run the chatbot locally?",
     "top_k": 3
   }
   ```
   - `top_k` (optional) controls how many relevant passages to retrieve before passing to the LLM.

2. **Endpoints**  
   - `GET /health` → returns `{"status": "ok"}` (simple health check).  
   - `POST /chat` → expects a JSON body:
     ```json
     {
       "question": "Your question here",
       "top_k": 5
     }
     ```
     Returns:
     ```json
     {
       "answer": "The LLM-generated response...",
       "sources": ["doc1.md", "guide.pdf"]
     }
     ```

---

## Project Structure

```
Doc Chatbot/
├── .venv/                   # (gitignored) your virtual environment
├── data/                    # (optional) raw documentation files to index
│   ├── getting_started.md
│   ├── architecture_overview.md
│   └── user_manual.pdf
├── embeddings/              # (optional) serialized embeddings / vector index files
│   └── index.faiss
├── main.py                  # entry point: FastAPI app
├── requirements.txt         # Python dependencies
├── Dockerfile               # (optional) containerize the app
├── README.md                # ← You’re here
├── utils.py                 # helper functions (e.g., loading docs, embedding logic)
└── .gitignore
```

- **`main.py`**  
  Contains the FastAPI application, routes, and dependency injection for your retrieval/LLM logic.

- **`utils.py`**  
  Functions to parse Markdown/PDF, create embeddings (if using), and handle caching.

- **`data/`**  
  Place all your documentation (Markdown, PDF) here so the chatbot can index them.

- **`embeddings/`**  
  If you use a vector-database (e.g., FAISS), serialized index files go here.  
  (This directory is optional—only if you choose retrieval via embeddings.)

- **`requirements.txt`**  
  Pin all Python packages needed, for example:
  ```
  fastapi==0.95.0
  uvicorn==0.22.0
  openai==0.30.0
  python-multipart==0.0.6
  PyPDF2==3.0.1
  sentence-transformers==2.2.2   # if using embeddings
  faiss-cpu==1.7.4              # if using FAISS
  ```

---

## Configuration

1. **Environment Variables**  
   - `OPENAI_API_KEY` (or any API key for your chosen LLM)  
   - `EMBEDDING_MODEL_NAME` (e.g., `all-MiniLM-L6-v2` if you’re using Hugging Face embeddings)  

2. **Configuration File (Optional)**  
   You can also load settings from a `config.json` or `config.yaml` placed at the root. Example:
   ```jsonc
   {
     "llm": {
       "provider": "openai",
       "model": "gpt-4o-mini",
       "temperature": 0.0
     },
     "retrieval": {
       "method": "embeddings",
       "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
       "index_path": "embeddings/index.faiss"
     },
     "paths": {
       "docs_folder": "data",
       "cache_folder": "cache"
     }
   }
   ```
   In `main.py`, you can read this file at startup and override defaults.

---

## Adding New Documentation Sources

1. **Place your files** (Markdown, PDF) in `data/`.  
2. If you’re using embeddings, **recompute or append** to your index:
   ```bash
   python utils.py --build-index
   ```
   (Assumes `utils.py` has a CLI entry point that reads from `data/` and writes to `embeddings/index.faiss`.)

3. **Restart** the server (`CTRL+C` → rerun `uvicorn main:app --reload`). The new docs will be available for querying.

---

## Troubleshooting

- **“ModuleNotFoundError: No module named 'fastapi'”**  
  → Make sure your venv is activated (`source .venv/bin/activate`) and that you ran `pip install -r requirements.txt`.

- **“ImportError: libfaiss.so: cannot open shared object file”** (Linux)  
  → You need the correct FAISS wheel; try `pip install faiss-cpu`. On macOS, `brew install faiss` then `pip install faiss-cpu`.

- **“openai.error.AuthenticationError”**  
  → Verify that `OPENAI_API_KEY` is set in your shell:  
  ```bash
  echo $OPENAI_API_KEY
  ```  
  If it’s empty, do `export OPENAI_API_KEY="your_key"` or add it to your shell profile.

- **Failed to parse PDF / corrupt files**  
  → Check that all PDFs in `data/` are not password-protected and can be read by `PyPDF2` (or whichever parser you use).

---

## Contributing

1. **Fork** the repo and create a feature branch:
   ```bash
   git checkout -b feature/your-improvement
   ```
2. **Implement** your changes, and add tests if appropriate.  
3. **Submit a Pull Request** against the `main` (or `master`) branch. Describe:
   - What you changed  
   - Why it’s useful  
   - Any backward-incompatible notes  
4. We’ll review, iterate, and merge.  

Please follow the existing [PEP 8](https://www.python.org/dev/peps/pep-0008/) style, and write clear docstrings for any new functions.

---

## License

This project is released under the **MIT License**. See [LICENSE](../LICENSE) for details.  
Feel free to use, modify, or distribute as you see fit.
