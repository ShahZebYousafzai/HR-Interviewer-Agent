import streamlit as st
from config.audio_config import AudioConfig
from audio.tts_manager import TTSManager

class AudioSidebar:
    """Audio configuration sidebar component with ElevenLabs integration"""
    
    def __init__(self):
        self.audio_config = AudioConfig()
    
    def render(self):
        """Render audio configuration sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.subheader("🎤 Voice Configuration")
            
            # Check API key
            import os
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                st.error("⚠️ ElevenLabs API key not found!")
                st.info("Set ELEVENLABS_API_KEY environment variable")
                return
            
            # Enable/disable voice
            voice_enabled = st.checkbox("Enable Voice Interaction", value=True)
            st.session_state.voice_enabled = voice_enabled
            
            if voice_enabled:
                self._render_tts_config()
                self._render_stt_config()
                self._render_api_status()
    
    def _render_tts_config(self):
        """Render TTS configuration"""
        st.subheader("🔊 Text-to-Speech")
        tts_enabled = st.checkbox("Enable TTS (AI speaks)", value=True)
        st.session_state.tts_enabled = tts_enabled
        
        if tts_enabled:
            st.info("🔊 Using ElevenLabs Neural Voices")
            
            # Voice selection
            selected_voice = st.selectbox(
                "Voice",
                options=list(self.audio_config.VOICE_OPTIONS.keys()),
                format_func=lambda x: self.audio_config.VOICE_OPTIONS[x],
                index=0
            )
            st.session_state.selected_voice = selected_voice
            
            # Advanced voice settings
            with st.expander("⚙️ Advanced Voice Settings"):
                # Speech speed
                speech_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
                st.session_state.speech_speed = speech_speed
                
                # Voice stability
                stability = st.slider("Voice Stability", 0.0, 1.0, 0.75, 0.05)
                st.session_state.voice_stability = stability
                
                # Similarity boost
                similarity = st.slider("Similarity Boost", 0.0, 1.0, 0.75, 0.05)
                st.session_state.voice_similarity = similarity
                
                # Style exaggeration
                style = st.slider("Style Exaggeration", 0.0, 1.0, 0.0, 0.1)
                st.session_state.voice_style = style
            
            # Test TTS
            if st.button("🎵 Test Voice"):
                self._test_tts(selected_voice, speech_speed)
    
    def _render_stt_config(self):
        """Render STT configuration"""
        st.subheader("🎤 Speech-to-Text")
        st.info("Using ElevenLabs STT with Whisper fallback")
        
        # STT model selection
        stt_model = st.selectbox(
            "STT Model",
            options=["eleven_multilingual_v2", "eleven_english_v1"],
            index=0
        )
        st.session_state.stt_model = stt_model
        
        # Language selection
        stt_language = st.selectbox(
            "Primary Language",
            options=["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh", "ja", "hi", "ko"],
            index=0
        )
        st.session_state.stt_language = stt_language
    
    def _render_api_status(self):
        """Render API status information"""
        st.subheader("📊 API Status")
        
        try:
            # Initialize TTS manager to check connection
            if not hasattr(st.session_state, 'tts_manager'):
                st.session_state.tts_manager = TTSManager()
            
            # Try to get available voices to test connection
            available_voices = st.session_state.tts_manager.get_available_voices()
            st.success(f"✅ Connected to ElevenLabs")
            st.info(f"🎭 {len(available_voices)} voices available")
            
            # Show usage info
            with st.expander("💡 Usage Information"):
                st.markdown("""
                **ElevenLabs Features:**
                - High-quality neural voices
                - Real-time speech synthesis
                - Multiple language support
                - Voice cloning capabilities
                
                **Free Tier Limits:**
                - 10,000 characters/month
                - 3 custom voices
                - Standard voice library
                """)
                
        except Exception as e:
            st.error(f"❌ ElevenLabs connection failed")
            st.error(f"Error: {str(e)}")
    
    def _test_tts(self, voice: str, speed: float):
        """Test TTS functionality"""
        test_text = "Hello! This is a test of the ElevenLabs text-to-speech system. How do I sound?"
        
        if not hasattr(st.session_state, 'tts_manager'):
            st.session_state.tts_manager = TTSManager()
        
        with st.spinner("Testing ElevenLabs voice..."):
            success = st.session_state.tts_manager.speak_text_sync(
                test_text, voice, speed
            )
            if success:
                st.success("🔊 ElevenLabs voice test successful!")
            else:
                st.error("❌ Voice test failed")
    
    def get_character_usage_estimate(self, text: str) -> int:
        """Estimate character usage for ElevenLabs billing"""
        # ElevenLabs charges per character
        return len(text.replace(' ', '').replace('\n', ''))