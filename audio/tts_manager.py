import os
import tempfile
import asyncio
import pygame
import edge_tts
import streamlit as st
from config.audio_config import AudioConfig
from utils.text_processing import TextProcessor
from core.exceptions import TTSError

class TTSManager:
    """Text-to-Speech management with Edge TTS"""
    
    def __init__(self):
        try:
            pygame.mixer.init()
            self.audio_config = AudioConfig()
            self.text_processor = TextProcessor()
        except Exception as e:
            raise TTSError(f"Failed to initialize TTS: {e}")
    
    def speak_text_sync(self, text: str, voice: str = "aria", speed: float = 1.0) -> bool:
        """Convert text to speech synchronously"""
        try:
            return asyncio.run(self._speak_text_async(text, voice, speed))
        except Exception as e:
            st.error(f"TTS Error: {e}")
            return False
    
    async def _speak_text_async(self, text: str, voice: str, speed: float) -> bool:
        """Convert text to speech asynchronously"""
        try:
            clean_text = self.text_processor.clean_text_for_speech(text)
            return await self._edge_tts(clean_text, voice)
        except Exception as e:
            raise TTSError(f"TTS processing failed: {e}")
    
    async def _edge_tts(self, text: str, voice: str) -> bool:
        """Edge TTS implementation"""
        try:
            voice_name = self.audio_config.get_edge_voice_name(voice)
            communicate = edge_tts.Communicate(text, voice_name)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_path = tmp_file.name

            await communicate.save(tmp_path)
            self._play_audio_file(tmp_path)
            os.unlink(tmp_path)

            return True
        except Exception as e:
            raise TTSError(f"Edge TTS error: {e}")
    
    def _play_audio_file(self, file_path: str):
        """Play audio file using pygame"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                asyncio.sleep(0.1)

            pygame.mixer.music.unload()
        except Exception as e:
            raise TTSError(f"Audio playback error: {e}")