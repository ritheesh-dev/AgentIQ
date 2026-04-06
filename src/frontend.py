import streamlit as st
import os
from RAG import ingest
import generation
from config import config

# --- Page Configuration ---
st.set_page_config(
    page_title="RAG Agent with Web Search",
    page_icon="🤖",
    layout="wide"
)
# --- Streamlit UI ---
def main():
    st.title("🤖 RAG Agent with Web Search")
    st.markdown("Ask questions about malaria or any health-related topics!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # PDF Ingestion Section
        st.subheader("📚 Knowledge Base")
        
        if os.path.exists(config.KNOWLEDGE_BASE_DIR):
            pdf_files = [f for f in os.listdir(config.KNOWLEDGE_BASE_DIR) if f.lower().endswith(".pdf")]
            st.info(f"Found {len(pdf_files)} PDF(s) in knowledge base")
            
            if pdf_files:
                with st.expander("View PDFs"):
                    for pdf in pdf_files:
                        st.text(f"📄 {pdf}")
        else:
            st.warning("Knowledge base directory not found")

    # Ingest Button
        if st.button("🔄 Ingest/Re-ingest PDFs", use_container_width=True):
            with st.spinner("Ingesting PDFs into vector database..."):
                doc_count = ingest.ingest_pdfs_into_vectordb()
                if doc_count > 0:
                    st.success(f"✅ Ingested {doc_count} documents!")
                    st.cache_resource.clear()
                else:
                    st.warning("No documents found to ingest")        

     # Database Status
        st.subheader("💾 Database Status")
        if os.path.exists(config.PERSIST_DIRECTORY):
            st.success("Vector database exists")
        else:
            st.error("Vector database not found. Please ingest PDFs.")
        
        st.divider()                

     # Information
        st.subheader("ℹ️ About")
        st.markdown("""
        This agent can:
        - 📖 Search local PDF documents
        - 🌐 Search the web for latest info
        - 🎯 Automatically route queries
        """)
    
    # Main Chat Interface
    st.divider()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source" in message:
                with st.expander("📚 Source"):
                    st.info(message["source"])    


     # Chat input
    if question := st.chat_input("Ask a question about malaria or health topics..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Build and run the graph
                    app = generation.build_graph()
                    inputs = {"question": question}
                    
                    # Stream the output
                    result = None
                    for output in app.stream(inputs, stream_mode="values"):
                        result = output
                    
                    if result and "answer" in result:
                        answer = result["answer"]
                        source_info = result.get("sender", "unknown")
                        
                        st.markdown(answer)
                        
                        # Show source information
                        if "documents" in result and result["documents"]:
                            sources = []
                            for doc in result["documents"]:
                                if "source" in doc.metadata:
                                    sources.append(doc.metadata["source"])
                            
                            if sources:
                                source_text = "Sources:\n" + "\n".join(f"- {s}" for s in sources)
                                with st.expander("📚 View Sources"):
                                    st.text(source_text)
                                
                                # Add to chat history with source
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": answer,
                                    "source": source_text
                                })
                            else:
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": answer
                                })
                        else:
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": answer
                            })
                    else:
                        error_msg = "I couldn't generate an answer. Please try again."
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
                
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
