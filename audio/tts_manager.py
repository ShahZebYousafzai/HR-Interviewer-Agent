import os
import tempfile
import asyncio
import pygame
import streamlit as st
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
from config.audio_config import AudioConfig
from utils.text_processing import TextProcessor
from core.exceptions import TTSError
from dotenv import load_dotenv

load_dotenv()

class TTSManager:
    """Text-to-Speech management with ElevenLabs API"""
    
    def __init__(self):
        try:
            pygame.mixer.init()
            self.audio_config = AudioConfig()
            self.text_processor = TextProcessor()
            
            # Initialize ElevenLabs client
            api_key = "sk_9f1dc8802fb4c1e1cdb9d023b12b285d2eed23a1aa19dbdd"
            if not api_key:
                raise TTSError("ElevenLabs API key not found. Please set ELEVENLABS_API_KEY environment variable.")
            
            self.client = ElevenLabs(api_key=api_key)
            self._available_voices = None
            
        except Exception as e:
            raise TTSError(f"Failed to initialize TTS: {e}")
    
    def speak_text_sync(self, text: str, voice: str = "rachel", speed: float = 1.0) -> bool:
        """Convert text to speech synchronously"""
        try:
            clean_text = self.text_processor.clean_text_for_speech(text)
            return self._elevenlabs_tts(clean_text, voice, speed)
        except Exception as e:
            st.error(f"TTS Error: {e}")
            return False
    
    def _elevenlabs_tts(self, text: str, voice: str, speed: float) -> bool:
        """ElevenLabs TTS implementation"""
        try:
            voice_id = self.audio_config.get_elevenlabs_voice_id(voice)
            
            # Get voice settings from config
            voice_settings = self.audio_config.get_voice_settings(voice)
            
            # Get custom settings from session state if available
            stability = getattr(st.session_state, 'voice_stability', voice_settings['stability'])
            similarity = getattr(st.session_state, 'voice_similarity', voice_settings['similarity_boost'])
            style = getattr(st.session_state, 'voice_style', voice_settings['style'])
            
            # Generate audio using the client
            audio_generator = self.client.text_to_speech.stream(
                text=text,
                voice_id=voice_id
            )

            stream(audio_generator)
            
            # # Convert generator to bytes
            # audio_bytes = b"".join(audio_generator)
            
            # # Save to temporary file and play
            # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            #     tmp_file.write(audio_bytes)
            #     tmp_path = tmp_file.name
            
            # self._play_audio_file(tmp_path)
            # os.unlink(tmp_path)
            
            return True
            
        except Exception as e:
            raise TTSError(f"ElevenLabs TTS error: {e}")
    
    def _play_audio_file(self, file_path: str):
        """Play audio file using pygame"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)  # Use pygame.time.wait instead of asyncio.sleep
            
            pygame.mixer.music.unload()
            
        except Exception as e:
            raise TTSError(f"Audio playback error: {e}")
    
    def get_available_voices(self):
        """Get available ElevenLabs voices"""
        try:
            if self._available_voices is None:
                voices = self.client.voices.get_all()
                self._available_voices = {
                    voice.voice_id: voice.name 
                    for voice in voices.voices
                }
            return self._available_voices
            
        except Exception as e:
            # Return default voices if API call fails
            return {
                "21m00Tcm4TlvDq8ikWAM": "Rachel",
                "AZnzlk1XvdvUeBnXmlld": "Domi",
                "EXAVITQu4vr4xnSDxMaL": "Bella",
                "MF3mGyEYCl7XYWbV9V6O": "Elli",
                "TxGEqnHWrfWFTfGW9XjX": "Josh",
                "VR6AewLTigWG4xSOukaG": "Arnold",
                "pNInz6obpgDQGcFmaJgB": "Adam",
                "yoZ06aMxZJJ28mfd3POQ": "Sam"
            }