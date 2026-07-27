import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from llm import embedding_model

BASE_DIR = Path(__file__).resolve().parent.parent
db_dir = str(BASE_DIR / "chroma_db")
pdf_path = BASE_DIR / "pdfs" / "academics_handbook.pdf"

academic_store = Chroma(
    collection_name="academic_info",
    embedding_function=embedding_model,
    persist_directory=db_dir,
)

if academic_store._collection.count() == 0 and pdf_path.exists():
    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    academic_store.add_documents(chunks)

academic_retriever = academic_store.as_retriever()