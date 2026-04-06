from langchain_huggingface import HuggingFaceEmbeddings
from RAG import ingest  
from langchain_community.vectorstores import Chroma
import os
from config import config
import streamlit as st

@st.cache_resource
def create_retriever():
    """Creates a retriever from the Chroma DB."""
    if not os.path.exists(config.PERSIST_DIRECTORY):
        return None
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory= config.PERSIST_DIRECTORY,
        embedding_function = embeddings
    )

    return vectorstore.as_retriever(search_kwargs={"k": 1})





