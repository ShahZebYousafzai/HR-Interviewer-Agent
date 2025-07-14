import os
import tempfile
import speech_recognition as sr
from typing import Optional
from core.exceptions import STTError

class STTManager:
    """Speech-to-Text management"""
    
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            raise STTError(f"Failed to initialize STT: {e}")
    
    def record_audio_streamlit(self, audio_data) -> Optional[str]:
        """Process audio from Streamlit audiorecorder"""
        try:
            if audio_data is None or len(audio_data) == 0:
                return None

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_path = tmp_file.name

            audio_data.export(tmp_path, format="wav")

            try:
                with sr.AudioFile(tmp_path) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.record(source)
                return self._google_stt(audio)
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            raise STTError(f"Audio processing error: {e}")
    
    def _google_stt(self, audio) -> Optional[str]:
        """Google Speech Recognition"""
        try:
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text.strip() if text else None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise STTError(f"Google STT service error: {e}")