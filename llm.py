from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser


chat_llm = ChatOllama(model = "granite4:3b")
embedding_model = OllamaEmbeddings(model = "all-minilm:33m")
parser = StrOutputParser()