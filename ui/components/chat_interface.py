import streamlit as st
from langchain.schema import HumanMessage, AIMessage

class ChatInterface:
    """Chat interface component with selective message display"""
    
    def render(self):
        """Render the main chat interface"""
        st.subheader("💬 Interview Chat")
        
        # Display chat history from conversation_history for better control
        conversation_history = st.session_state.state.get("conversation_history", [])
        
        if conversation_history:
            for exchange in conversation_history:
                # Only show user messages that aren't the initial hidden hello
                if exchange["user"] != "Hello" or len(conversation_history) > 1:
                    with st.chat_message("user"):
                        st.write(exchange["user"])
                
                with st.chat_message("assistant"):
                    st.write(exchange["assistant"])
        else:
            # If no conversation history but we have messages, show only AI responses
            messages = st.session_state.state.get("messages", [])
            for message in messages:
                if isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)
        
        # Show current interview stage
        stage = st.session_state.state.get("interview_stage", "greeting")
        if stage == "greeting":
            st.info("👋 Welcome! The interview is about to begin...")
        elif stage == "profile_collection":
            st.info("📝 Please share your professional background...")
        elif stage == "interview":
            st.info("🎯 Interview in progress...")
        elif stage == "ended":
            st.success("✅ Interview completed!")
    
    def display_only_ai_responses(self):
        """Alternative method to display only AI responses"""
        messages = st.session_state.state.get("messages", [])
        
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)