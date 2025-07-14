import streamlit as st
from config.settings import CONFIG
from utils.session_manager import SessionManager
from workflow.graph_builder import create_enhanced_chat_graph
from audio.tts_manager import TTSManager
from audio.stt_manager import STTManager
from ui.app import StreamlitApp
from core.exceptions import InterviewSystemError

def initialize_system():
    """Initialize the complete system"""
    if "graph" not in st.session_state:
        try:
            with st.spinner("🚀 Initializing HR Interview System..."):
                # Initialize components
                st.session_state.graph = create_enhanced_chat_graph("llama3.2")
                st.session_state.tts_manager = TTSManager()
                st.session_state.stt_manager = STTManager()
                
                st.success("✅ System initialized successfully!")
                return True
        except Exception as e:
            st.error(f"❌ System initialization failed: {e}")
            st.info("💡 Make sure Ollama is running with: `ollama serve` and `ollama pull llama3.2`")
            
            # Show detailed error in debug mode
            if CONFIG.debug:
                st.exception(e)
            
            return False
    return True

def main():
    """Main application entry point"""
    try:
        # Configure Streamlit
        st.set_page_config(
            page_title=CONFIG.page_title,
            page_icon=CONFIG.page_icon,
            layout=CONFIG.layout
        )
        
        # Initialize session state
        SessionManager.initialize_session_state()
        
        # Initialize system
        if not initialize_system():
            st.stop()
        
        # Run the Streamlit app
        app = StreamlitApp()
        app.run()
        
    except InterviewSystemError as e:
        st.error(f"Interview System Error: {e}")
        if CONFIG.debug:
            st.exception(e)
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        if CONFIG.debug:
            st.exception(e)

if __name__ == "__main__":
    main()