import streamlit as st
from datetime import datetime
from langchain.schema import HumanMessage

from ui.components.audio_sidebar import AudioSidebar
from ui.components.chat_interface import ChatInterface
from ui.components.voice_input import VoiceInput
from ui.components.status_display import StatusDisplay
from ui.components.profile_analysis import ProfileAnalysisDisplay
from utils.session_manager import SessionManager
from utils.timer import TimerUtils

class StreamlitApp:
    """Main Streamlit application with auto-initialize"""
    
    def __init__(self):
        self.audio_sidebar = AudioSidebar()
        self.chat_interface = ChatInterface()
        self.voice_input = VoiceInput()
        self.status_display = StatusDisplay()
        self.profile_display = ProfileAnalysisDisplay()
    
    def run(self):
        """Run the Streamlit application"""
        st.title("HR Interview System")
        st.markdown("*AI-powered interviews with Llama3.2 and Edge TTS*")
        
        # Render sidebar configuration
        self._render_sidebar()
        
        # Update session state
        self._update_session_state()
        
        # Auto-initialize the interview with hidden hello
        self._auto_initialize_interview()
        
        # Render main interface
        self.status_display.render()
        self.profile_display.render()
        self.chat_interface.render()
        self.voice_input.render()
        
        # Handle text input
        self._handle_text_input()
        
        # Handle pending TTS
        self._handle_pending_tts()
    
    def _auto_initialize_interview(self):
        """Auto-initialize the interview if not already done"""
        if hasattr(st.session_state, 'graph'):
            # Check if we need to auto-initialize
            auto_initialized = SessionManager.auto_initialize_interview()
            
            if auto_initialized and not hasattr(st.session_state, '_initial_rerun_done'):
                # Mark that we've done the initial rerun to avoid infinite loops
                st.session_state._initial_rerun_done = True
                # Rerun to display the AI's welcome message
                st.rerun()
    
    def _render_sidebar(self):
        """Render sidebar components"""
        with st.sidebar:
            st.subheader("🔧 Configuration")
            
            # Timer configuration
            st.subheader("⏰ Interview Timer")
            interview_duration = st.slider(
                "Duration (minutes)", 
                min_value=5, 
                max_value=120, 
                value=30, 
                step=5
            )
            
            # System status
            st.subheader("📊 System Status")
            st.success("🤖 Model: Llama3.2")
            st.success("🔊 TTS: ElevenLabs TTS")
            st.success("🎤 STT: Google Speech Recognition")
            st.success("🎙️ Voice: Auto-Enabled")
            
            # Store duration
            st.session_state.interview_duration = interview_duration
        
        # Audio configuration
        self.audio_sidebar.render()
        
        # Debug section
        self._render_debug_sidebar()
    
    def _render_debug_sidebar(self):
        """Render debug information in sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.subheader("🐛 Debug Info")
            
            if "state" in st.session_state:
                state = st.session_state.state
                st.write(f"**Stage:** {state['interview_stage']}")
                st.write(f"**Messages:** {len(state['messages'])}")
                st.write(f"**Questions:** {len(state.get('question_bank', []))}")
                st.write(f"**Ended:** {state.get('is_interview_ended', False)}")
                st.write(f"**Auto-Init:** {state.get('auto_initialized', False)}")
                
                if state.get("interview_start_time"):
                    elapsed = datetime.now() - state["interview_start_time"]
                    st.write(f"**Elapsed:** {TimerUtils.format_time(elapsed)}")

            if st.button("🔄 Reset Interview"):
                # Clear the auto-init flag when resetting
                if hasattr(st.session_state, '_initial_rerun_done'):
                    del st.session_state._initial_rerun_done
                SessionManager.reset_interview()
                st.rerun()
    
    def _update_session_state(self):
        """Update session state with current settings"""
        st.session_state.state["interview_duration"] = getattr(st.session_state, 'interview_duration', 30)
        st.session_state.state["voice_enabled"] = getattr(st.session_state, 'voice_enabled', False)
    
    def _handle_text_input(self):
        """Handle text input for non-ended interviews"""
        if not st.session_state.state.get("is_interview_ended", False):
            user_input = st.chat_input("Type your message here...")

            if user_input:
                st.session_state.state["messages"].append(HumanMessage(content=user_input))

                with st.spinner("🤖 Thinking..."):
                    try:
                        result = st.session_state.graph.invoke(st.session_state.state)
                        st.session_state.state = result
                        self._mark_tts_response()
                        
                    except Exception as e:
                        st.error(f"Error processing message: {e}")

                st.rerun()
        else:
            st.info("💬 Interview has ended. Thank you for participating!")
    
    def _mark_tts_response(self):
        """Mark message for TTS but defer playback"""
        from langchain.schema import AIMessage
        
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
    
    def _handle_pending_tts(self):
        """Handle pending TTS playback"""
        if hasattr(st.session_state, "pending_tts"):
            pending = st.session_state.pending_tts
            with st.spinner("🔊 AI is speaking..."):
                success = st.session_state.tts_manager.speak_text_sync(
                    pending["text"], pending["voice"], pending["speed"]
                )
            del st.session_state.pending_tts  # Clear after use