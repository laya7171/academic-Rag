import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from llm import embedding_model

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
db_dir = str(BASE_DIR / "chroma_db")
env_pdf_path = os.getenv("FEE_PATH")
pdf_path = Path(env_pdf_path) if env_pdf_path and os.path.exists(env_pdf_path) else (BASE_DIR / "pdfs" / "fee_structure.pdf")

fee_store = Chroma(
    collection_name="fee_structure",
    embedding_function=embedding_model,
    persist_directory=db_dir,
)

if fee_store._collection.count() == 0 and pdf_path.exists():
    doc_loader = PyPDFLoader(str(pdf_path))
    docs = doc_loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    fee_store.add_documents(chunks)

fee_retriever = fee_store.as_retriever()