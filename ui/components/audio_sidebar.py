import streamlit as st
from config.audio_config import AudioConfig
from audio.tts_manager import TTSManager

class AudioSidebar:
    """Audio configuration sidebar component"""
    
    def __init__(self):
        self.audio_config = AudioConfig()
    
    def render(self):
        """Render audio configuration sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.subheader("🎤 Voice Configuration")
            
            # Enable/disable voice
            voice_enabled = st.checkbox("Enable Voice Interaction", value=True)
            st.session_state.voice_enabled = voice_enabled
            
            if voice_enabled:
                self._render_tts_config()
                self._render_stt_config()
    
    def _render_tts_config(self):
        """Render TTS configuration"""
        st.subheader("🔊 Text-to-Speech")
        tts_enabled = st.checkbox("Enable TTS (AI speaks)", value=True)
        st.session_state.tts_enabled = tts_enabled
        
        if tts_enabled:
            st.info("🔊 Using Microsoft Edge TTS")
            
            # Voice selection
            selected_voice = st.selectbox(
                "Voice",
                options=list(self.audio_config.VOICE_OPTIONS.keys()),
                format_func=lambda x: self.audio_config.VOICE_OPTIONS[x],
                index=0
            )
            st.session_state.selected_voice = selected_voice
            
            # TTS Settings
            st.subheader("⚙️ Settings")
            speech_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
            st.session_state.speech_speed = speech_speed
            
            # Test TTS
            if st.button("🎵 Test Voice"):
                self._test_tts(selected_voice, speech_speed)
    
    def _render_stt_config(self):
        """Render STT configuration"""
        st.subheader("🎤 Speech-to-Text")
        st.info("Using Google Speech Recognition (Free)")
    
    def _test_tts(self, voice: str, speed: float):
        """Test TTS functionality"""
        test_text = "Hello! This is a test of the text-to-speech system."
        
        if not hasattr(st.session_state, 'tts_manager'):
            st.session_state.tts_manager = TTSManager()
        
        with st.spinner("Testing voice..."):
            success = st.session_state.tts_manager.speak_text_sync(
                test_text, voice, speed
            )
            if success:
                st.success("🔊 Voice test successful!")
            else:
                st.error("❌ Voice test failed")