import streamlit as st
from app import OrangeChatbot
import time

# Set page config
st.set_page_config(
    page_title="Orange Tunisia Chatbot",
    page_icon="🍊",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chatbot = OrangeChatbot()

# Sidebar with app info
with st.sidebar:
    st.title("🍊 Orange Tunisia Chatbot")
    st.markdown("""
    ### About
    This chatbot can answer questions about Orange Tunisia's products and services using RAG.
    
    **Note:** The first query might take longer as it loads the models.
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
st.title("🍊 Orange Tunisia Chatbot")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Orange Tunisia..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            try:
                # Get response from chatbot
                response = st.session_state.chatbot.get_response(prompt)
                full_response = response["answer"]
                
                # Stream the response
                for chunk in full_response.split():
                    full_response_chunk = chunk + " "
                    message_placeholder.markdown(full_response_chunk + "▌")
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response_chunk)
                
                # Show sources
                with st.expander("View sources"):
                    for i, source in enumerate(response["sources"], 1):
                        st.markdown(f"**Source {i}**")
                        st.json(source["metadata"])
                        st.text_area(f"Content {i}", value=source["content"], height=150)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                full_response = "I'm sorry, I encountered an error while processing your request."
                message_placeholder.markdown(full_response)
    
    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})