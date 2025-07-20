import os
import tempfile
import io
from typing import Optional
from elevenlabs.client import ElevenLabs
from core.exceptions import STTError
from dotenv import load_dotenv

load_dotenv()

class STTManager:
    """Speech-to-Text management with ElevenLabs API"""
    
    def __init__(self):
        try:
            # Initialize ElevenLabs client
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                raise STTError("ElevenLabs API key not found. Please set ELEVENLABS_API_KEY environment variable.")
            
            self.client = ElevenLabs(api_key=api_key)
            
        except Exception as e:
            raise STTError(f"Failed to initialize STT: {e}")
    
    def record_audio_streamlit(self, audio_data) -> Optional[str]:
        """Process audio from Streamlit audiorecorder using ElevenLabs STT"""
        try:
            if audio_data is None or len(audio_data) == 0:
                return None

            # Save audio to temporary file for ElevenLabs STT
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_path = tmp_file.name
            
            audio_data.export(tmp_path, format="wav")

            try:
                # Use ElevenLabs speech-to-text
                with open(tmp_path, "rb") as audio_file:
                    transcript = self.client.speech_to_text.convert_as_stream(
                        audio_file,
                        model_id="eleven_multilingual_v2"
                    )
                
                # Collect all chunks from the stream
                transcript_text = ""
                for chunk in transcript:
                    if hasattr(chunk, 'text'):
                        transcript_text += chunk.text
                
                os.unlink(tmp_path)
                return transcript_text.strip() if transcript_text else None
                
            except Exception as e:
                os.unlink(tmp_path)
                # Fallback to OpenAI Whisper if ElevenLabs STT fails
                return self._fallback_whisper_stt(audio_data)

        except Exception as e:
            raise STTError(f"Audio processing error: {e}")
    
    def _fallback_whisper_stt(self, audio_data) -> Optional[str]:
        """Fallback to OpenAI Whisper API for STT"""
        try:
            import openai
            
            # Check for OpenAI API key
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                raise STTError("No fallback STT available. Please set OPENAI_API_KEY for Whisper fallback.")
            
            client = openai.OpenAI(api_key=openai_key)
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_path = tmp_file.name
            
            audio_data.export(tmp_path, format="wav")
            
            try:
                with open(tmp_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"
                    )
                return transcript.text.strip() if transcript.text else None
                
            finally:
                os.unlink(tmp_path)
                
        except Exception as e:
            raise STTError(f"Fallback Whisper STT error: {e}")
    
    def transcribe_file(self, file_path: str) -> Optional[str]:
        """Transcribe audio file using ElevenLabs STT"""
        try:
            with open(file_path, "rb") as audio_file:
                transcript = self.client.speech_to_text.convert_as_stream(
                    audio_file,
                    model_id="eleven_multilingual_v2"
                )
            
            # Collect all chunks from the stream
            transcript_text = ""
            for chunk in transcript:
                if hasattr(chunk, 'text'):
                    transcript_text += chunk.text
            
            return transcript_text.strip() if transcript_text else None
            
        except Exception as e:
            raise STTError(f"File transcription error: {e}")