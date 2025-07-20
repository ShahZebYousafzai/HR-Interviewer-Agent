import streamlit as st
from datetime import datetime
from langchain.schema import HumanMessage, AIMessage
from core.types import ChatState

class SessionManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize session state variables"""
        if "state" not in st.session_state:
            st.session_state.state = {
                "messages": [],
                "current_question": "",
                "interview_stage": "greeting",
                "candidate_info": {},
                "conversation_history": [],
                "profile_analysis": {},
                "question_bank": [],
                "interview_start_time": None,
                "interview_duration": 30,
                "is_interview_ended": False,
                "voice_enabled": True,
                "selected_voice": "aria",
                "auto_initialized": False,  # New flag to track auto-initialization
            }
        
        # Set default voice settings
        defaults = {
            'voice_enabled': True,
            'tts_enabled': True,
            'selected_voice': "aria",
            'speech_speed': 1.0
        }
        
        for key, value in defaults.items():
            if not hasattr(st.session_state, key):
                setattr(st.session_state, key, value)
    
    @staticmethod
    def auto_initialize_interview():
        """Auto-initialize the interview with a hidden hello message"""
        if (not st.session_state.state.get("auto_initialized", False) and 
            hasattr(st.session_state, 'graph')):
            
            # Add hidden hello message (won't be displayed)
            hidden_hello = HumanMessage(content="Hello")
            st.session_state.state["messages"].append(hidden_hello)
            
            try:
                # Process the hello message through the graph
                result = st.session_state.graph.invoke(st.session_state.state)
                st.session_state.state = result
                
                # Mark as auto-initialized
                st.session_state.state["auto_initialized"] = True
                
                # Remove the hidden hello message from display
                # Keep only AI response for display
                if len(st.session_state.state["messages"]) >= 2:
                    # Remove the first human message (hello) but keep AI response
                    ai_response = st.session_state.state["messages"][-1]
                    st.session_state.state["messages"] = [ai_response]
                
                # Trigger TTS for the welcome message if enabled
                SessionManager._trigger_initial_tts()
                
                return True
                
            except Exception as e:
                st.error(f"Error during auto-initialization: {e}")
                # Reset if failed
                st.session_state.state["auto_initialized"] = False
                st.session_state.state["messages"] = []
                return False
        
        return st.session_state.state.get("auto_initialized", False)
    
    @staticmethod
    def _trigger_initial_tts():
        """Trigger TTS for the initial AI response"""
        if (getattr(st.session_state, 'tts_enabled', False) and
            hasattr(st.session_state, 'tts_manager') and
            st.session_state.tts_manager and
            st.session_state.state["messages"]):

            latest_message = st.session_state.state["messages"][-1]
            if isinstance(latest_message, AIMessage):
                st.session_state.pending_tts = {
                    "text": latest_message.content,
                    "voice": getattr(st.session_state, 'selected_voice', 'rachel'),
                    "speed": getattr(st.session_state, 'speech_speed', 1.0),
                }
    
    @staticmethod
    def reset_interview():
        """Reset interview while keeping system initialized"""
        keys_to_keep = [
            'graph', 'tts_manager', 'stt_manager', 
            'voice_enabled', 'tts_enabled', 
            'selected_voice', 'speech_speed'
        ]
        
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        
        SessionManager.initialize_session_state()
    
    @staticmethod
    def get_state() -> ChatState:
        """Get current chat state"""
        return st.session_state.state
    
    @staticmethod
    def update_state(new_state: ChatState):
        """Update chat state"""
        st.session_state.state = new_state