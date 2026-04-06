from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WebBaseLoader
from langgraph.graph import StateGraph,START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from RAG import retrieve
from config import config
import streamlit as st
load_dotenv()

#----Graph State Definnition----

class GraphState(TypedDict):
    question: str
    documents: List[Document]
    sender: str
    answer: str

def router_node(state: GraphState) -> str:
    """The Router. Decides which tool to use next."""
    question = state["question"]
    routing_prompt =  f"""You are an expert at routing user questions. 
    The **vectorstore** contains documents about **RAG ,AI , History of AI, Types of AI**. The **web_search** tool can access real-time information about AI jobs, fresher jobs information from linkedin. 
    Based on the user's question, decide whether it's best to use the vectorstore or the web search.
    Question: "{question}" Respond with only 'vectorstore' or 'web_search'."""

    llm = ChatGroq(temperature=0, model_name=config.LLM_MODEL_ID)
    response = llm.invoke(routing_prompt)
    decision = response.content.strip().lower()
    return "web_search" if "web_search" in decision else "vectorstore"

def retrieve_node(state: GraphState) -> str:
    """Retrieves documents from the vectorstore For AI releted Questions."""
    question = state["question"]
    retriever = retrieve.create_retriever()
    if retriever is None:
        return {"documents": [], "sender": "retrieve_node"}
    retrieved_docs = retriever.invoke(question)
    return {"documents": retrieved_docs, "sender": "retrieve_node"}

def web_search_node(state: GraphState) -> str:
    """Searches the web for Recent job information about fresher, then scrapes the content from the resulting URLs.""" 
    question = state["question"]
    tavily_search = TavilySearch(
        max_results=1, 
        search_depth="basic", 
        include_domains=[".linkedin.com"]
    )
    search_results = tavily_search.invoke(question)

    scraped_docs = []
    if not search_results or "results" not in search_results:
        return {"documents": [], "sender": "web_search_node"}
    
    urls = [result.get("url") for result in search_results["results"] if result.get("url")]
    
    if not urls:
        return {"documents": [], "sender": "web_search_node"}
    
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = url
            scraped_docs.extend(docs)
        except Exception as e:
            st.warning(f"Error scraping {url}: {e}")
    
    return {"documents": scraped_docs, "sender": "web_search_node"}

def generate_node(state: GraphState) -> GraphState:
    """Generates an answer using the LLM."""
    question = state["question"]
    documents = state["documents"]
    context = "\n\n".join(doc.page_content for doc in documents)
    prompt = f"""You are an expert Q&A assistant. Use the following context to answer the user's question. If the context does not contain the answer, state that you cannot find the information. Be concise and helpful. Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"""
    llm = ChatGroq(temperature=0, model_name=config.LLM_MODEL_ID)
    response = llm.invoke(prompt)
    answer = response.content
    return {"answer": answer, "sender": "generate_node"}


# --- Build the Graph ---

def build_graph():
    """Builds and compiles the workflow graph."""
    workflow = StateGraph(GraphState)
    
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generate", generate_node)
    
    workflow.add_conditional_edges(
        START,
        router_node,
        {
            "vectorstore": "retrieve",
            "web_search": "web_search",
        },
    )
    
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()
