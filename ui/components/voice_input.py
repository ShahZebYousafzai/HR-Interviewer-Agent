import time
import streamlit as st
from audiorecorder import audiorecorder
from langchain.schema import HumanMessage
from audio.stt_manager import STTManager

class VoiceInput:
    """Voice input component"""
    
    def render(self):
        """Render voice input interface"""
        if (st.session_state.state.get("voice_enabled", False) and 
            not st.session_state.state.get("is_interview_ended", False)):

            # Audio recorder
            audio = audiorecorder("🎤 Click to Record", "🛑 Recording...", key="audio_recorder")

            if len(audio) > 0:
                self._process_audio(audio)

    def _process_audio(self, audio):
        """Process recorded audio"""
        # Create unique audio ID
        audio_hash = hash(audio.export().read()[:100])
        audio_id = f"audio_{len(audio)}_{audio_hash}"

        if st.session_state.get("last_processed_audio_id") != audio_id:
            st.session_state.last_processed_audio_id = audio_id
            st.audio(audio.export().read())

            with st.spinner("🎯 Processing your voice response..."):
                try:
                    if not hasattr(st.session_state, 'stt_manager'):
                        st.session_state.stt_manager = STTManager()

                    text = st.session_state.stt_manager.record_audio_streamlit(audio)

                    if text:
                        st.success(f"✅ Heard: '{text}'")
                        st.session_state.state["messages"].append(HumanMessage(content=text))

                        if hasattr(st.session_state, 'graph'):
                            with st.spinner("🤖 AI is responding..."):
                                result = st.session_state.graph.invoke(st.session_state.state)
                                st.session_state.state = result
                                self._handle_tts_response()
                        else:
                            st.warning("System not ready")

                        time.sleep(0.3)
                        st.rerun()
                    else:
                        st.warning("❌ Could not understand audio. Please try again.")

                except Exception as e:
                    st.error(f"Speech recognition error: {e}")
        else:
            st.audio(audio.export().read())

    def _handle_tts_response(self):
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
                    "voice": st.session_state.selected_voice,
                    "speed": st.session_state.speech_speed,
                }