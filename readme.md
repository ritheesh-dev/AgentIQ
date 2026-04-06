# 🤖 AgenticIQ

> An intelligent, agentic RAG (Retrieval-Augmented Generation) system that routes user queries between a local knowledge base and real-time web search — powered by LangGraph, Groq, and Streamlit.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## 🧠 Overview

**AgenticIQ** is a full-stack agentic RAG pipeline that intelligently decides how to answer user questions. It uses a **router node** powered by an LLM to determine whether to retrieve documents from a local **ChromaDB vector store** or perform a **live web search** via Tavily — giving users the best of both worlds: deep domain knowledge and real-time information.

---

## ✨ Features

- 🔀 **Intelligent Routing** — LLM-based router decides between vector store and web search
- 📚 **RAG Pipeline** — Ingests and retrieves documents from ChromaDB
- 🌐 **Web Search** — Real-time search using Tavily API
- ⚡ **Fast Inference** — Powered by Groq's ultra-fast LLM API
- 🖥️ **Streamlit UI** — Clean, interactive frontend for querying the agent
- 🔗 **LangGraph Orchestration** — Robust agentic workflow using graph-based state management

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Groq (LLaMA / Mixtral) |
| **Orchestration** | LangGraph, LangChain |
| **Vector Store** | ChromaDB |
| **Embeddings** | HuggingFace |
| **Web Search** | Tavily API |
| **Frontend** | Streamlit |
| **Language** | Python 3.12 |

---

## 📁 Project Structure

```
Nexcus Agentic AI/
├── src/
│   ├── RAG/
│   │   ├── __init__.py
│   │   ├── ingest.py        # PDF ingestion & vector store creation
│   │   └── retrieve.py      # Document retrieval from ChromaDB
│   ├── __init__.py
│   ├── config.py            # Centralized configuration & env variables
│   ├── frontend.py          # Streamlit UI
│   └── generation.py        # LangGraph agent nodes & routing logic
├── knowledge-base/          # Source PDF documents (not tracked in git)
├── chroma_db/               # Persistent vector store (not tracked in git)
├── .env.example             # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Groq API Key](https://console.groq.com/)
- [Tavily API Key](https://tavily.com/)
- [HuggingFace Token](https://huggingface.co/settings/tokens)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/agenticiq.git
cd agenticiq
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Fill in your API keys in the `.env` file (see [Environment Variables](#environment-variables)).

### 5. Ingest your documents

Add your PDF files to the `knowledge-base/` folder, then run:

```bash
python -c "from src.RAG.ingest import ingest_pdfs_into_vectordb; ingest_pdfs_into_vectordb()"
```

### 6. Run the app

```bash
streamlit run src/frontend.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
USER_AGENT=your_user_agent_string
HF_TOKEN=your_huggingface_token
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## ⚙️ How It Works

```
User Query
    │
    ▼
┌─────────────┐
│ Router Node │  ← LLM decides: vectorstore or web_search?
└─────────────┘
     │          │
     ▼          ▼
┌─────────┐  ┌────────────┐
│   RAG   │  │ Web Search │
│Retrieve │  │  (Tavily)  │
└─────────┘  └────────────┘
     │          │
     └────┬─────┘
          ▼
   ┌─────────────┐
   │  Generation │  ← LLM generates final answer
   └─────────────┘
          │
          ▼
      Response
```

1. **Ingest** — PDFs are chunked, embedded, and stored in ChromaDB
2. **Route** — The router LLM analyzes the query and picks the best source
3. **Retrieve** — Documents are fetched from ChromaDB or Tavily web search
4. **Generate** — The LLM generates a final, grounded response
5. **Display** — Answer is shown in the Streamlit UI

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "feat: add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Built with ❤️ using LangChain, LangGraph, Groq & Streamlit | AgenticIQ
</div>