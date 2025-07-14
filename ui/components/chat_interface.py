import streamlit as st

class ChatInterface:
    """Chat interface component"""
    
    def render(self):
        """Render the main chat interface"""
        st.subheader("💬 Interview Chat")
        
        # Display chat history
        for exchange in st.session_state.state["conversation_history"]:
            with st.chat_message("user"):
                st.write(exchange["user"])
            with st.chat_message("assistant"):
                st.write(exchange["assistant"])
