from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
import streamlit as st
from config import config

# --- Load Environment Variables ---
load_dotenv()


# --- RAG Functions ---
def ingest_pdfs_into_vectordb():

    """Ingests PDFs into Chroma VectorDB."""

    documents = []
    if not os.path.exists(config.KNOWLEDGE_BASE_DIR):
        return 0
    
    for file_name in os.listdir(config.KNOWLEDGE_BASE_DIR):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(config.KNOWLEDGE_BASE_DIR, file_name)
            try:
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            except Exception as e:
                st.warning(f"Error loading {file_path}: {e}")

    if not documents:
        st.error("❌ No documents loaded")
        return 0            


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = config.CHUNK_SIZE,
        chunk_overlap = config.CHUNK_OVERLAP
    )

    text = text_splitter.split_documents(documents)

    if not text:
        st.error("❌ No text chunks created from PDFs")
        return 0
    
    embeddings =  HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=text,
        embedding=embeddings,
        persist_directory=config.PERSIST_DIRECTORY
    )

    return len(documents)

    