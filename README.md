# Academic Assistant RAG System

An intelligent, multi-agent Retrieval-Augmented Generation (RAG) system built with **LangGraph**, **LangChain**, **ChromaDB**, **Streamlit**, and **Ollama**.

The system dynamically classifies student inquiries into **Academic**, **Fee**, or **General** categories, routes queries to specialized vector retrieval nodes, and generates context-aware answers tailored to the user's selected academic program.

---

## 🌟 Key Features

- **Dynamic Query Classification**: Automatically categorizes incoming questions as `academic`, `fee`, or `general`.
- **Specialized RAG Routes**: 
  - **Academic Node**: Retrieves information from `academics_handbook.pdf`.
  - **Fee Structure Node**: Retrieves information from `fee_structure.pdf`.
  - **General Query Node**: Responds to greetings and general conversation.
- **Program-Aware Answers**: Formulates responses with context tailored to selected academic programs (`CSIT`, `BCA`, `BBA`).
- **Interactive Streamlit Interface**: Clean, modern web app UI with real-time chat history.
- **Efficient Vector Storage**: Uses persistent **Chroma DB** collections with automatic one-time document ingestion.

---

## 📁 Project Architecture

```
academic_rag/
├── app.py                      # Streamlit frontend UI
├── graph.py                    # LangGraph StateGraph & workflow execution
├── llm.py                      # Ollama LLM and Embeddings configuration
├── requirements.txt            # Dependencies list
├── .env                        # Environment variables configuration
├── schema/
│   ├── __init__.py
│   └── state.py                # LangGraph State schema with message reducer
├── nodes/
│   ├── classifier_node.py      # LLM query intent classifier
│   ├── router_node.py          # Conditional edge routing logic
│   ├── academic_rag_node.py    # Academic RAG context retriever & generator
│   ├── fee_rag_node.py         # Fee RAG context retriever & generator
│   └── general_query_node.py   # General conversational node
├── ingestion/
│   ├── __init__.py
│   ├── academic_ingestion.py   # Ingestion & Chroma retriever for Academic handbook
│   └── fee_ingestion.py        # Ingestion & Chroma retriever for Fee structure
├── pdfs/
│   ├── academics_handbook.pdf  # Academic reference PDF document
│   └── fee_structure.pdf       # Fee reference PDF document
└── chroma_db/                  # Persistent Chroma vector store
```

---

## ⚙️ Workflow Architecture

```
               [ User Input ]
                     │
                     ▼
             [ classifier_node ]
                     │
                     ▼
              [ router_node ]
           /         |         \
          /          |          \
   (academic)      (fee)      (general)
      │              │            │
      ▼              ▼            ▼
[academic_node]  [fee_node]  [general_node]
      │              │            │
      └──────────────┴────────────┘
                     │
                     ▼
                  [ END ]
```

---

## 🚀 Prerequisites

1. **Python 3.10+**
2. **Ollama** installed and running locally with the following models:
   - LLM: `granite4:3b`
     ```bash
     ollama pull granite4:3b
     ```
   - Embedding Model: `all-minilm:33m`
     ```bash
     ollama pull all-minilm:33m
     ```

---

## 🛠️ Setup & Installation

1. **Activate Existing Virtual Environment** (Windows PowerShell):
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Verify Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Ensure Ollama Service is Active**:
   ```powershell
   ollama list
   ```

---

## 🏃 Running the Application

Launch the Streamlit web application:

```powershell
.\venv\Scripts\streamlit.exe run app.py
```

Open your browser at `http://localhost:8501`.

1. Select your academic program (`CSIT`, `BCA`, or `BBA`).
2. Ask your question in the chat input (e.g., *"What are the attendance requirements?"* or *"What is the tuition fee structure?"*).

---

## 📄 Document Ingestion

Document ingestion runs automatically on first launch if `chroma_db` is unpopulated:
- `pdfs/academics_handbook.pdf` -> `academic_info` collection
- `pdfs/fee_structure.pdf` -> `fee_structure` collection

Subsequent runs instantly reuse the persistent vector collections without re-embedding.
