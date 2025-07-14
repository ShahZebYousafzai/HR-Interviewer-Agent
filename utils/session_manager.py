import streamlit as st
from datetime import datetime
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
