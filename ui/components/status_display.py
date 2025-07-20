import streamlit as st
from datetime import datetime
from utils.timer import TimerUtils

class StatusDisplay:
    """Status and timer display component"""
    
    def render(self):
        """Render timer and status information"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info("🤖 Using: Llama3.2")
        
        with col2:
            self._render_timer()
        
        with col3:
            self._render_voice_status()

    def _render_timer(self):
        """Render timer display"""
        start_time = st.session_state.state.get("interview_start_time")
        duration = st.session_state.state.get("interview_duration", 30)
        is_ended = st.session_state.state.get("is_interview_ended", False)
        
        if start_time and not is_ended:
            remaining_time = TimerUtils.get_remaining_time(start_time, duration)
            time_str = TimerUtils.format_time(remaining_time)
            
            if remaining_time.total_seconds() <= 0:
                st.error(f"⏰ Time's Up! 00:00")
            elif remaining_time.total_seconds() <= 300:  # Last 5 minutes
                st.warning(f"⏰ Time Left: {time_str}")
            else:
                st.info(f"⏰ Time Left: {time_str}")
        elif is_ended:
            st.error("⏰ Interview Ended")
        else:
            st.info(f"⏰ Duration: {duration} minutes")

    def _render_voice_status(self):
        """Render voice status"""
        if st.session_state.state.get("voice_enabled", False):
            if getattr(st.session_state, 'tts_enabled', False):
                st.success("🔊 TTS: ElevenLabs TTS")
            else:
                st.info("🎤 Voice: STT Only")
        else:
            st.info("🔇 Voice: OFF")
