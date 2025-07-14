from dataclasses import dataclass
from typing import Dict

@dataclass
class AudioConfig:
    """Audio configuration settings"""
    
    VOICE_OPTIONS: Dict[str, str] = None
    DEFAULT_VOICE: str = "aria"
    DEFAULT_SPEED: float = 1.0
    MIN_SPEED: float = 0.5
    MAX_SPEED: float = 2.0
    
    def __post_init__(self):
        if self.VOICE_OPTIONS is None:
            self.VOICE_OPTIONS = {
                "aria": "Aria (Female US)",
                "guy": "Guy (Male US)", 
                "jenny": "Jenny (Female US)",
                "davis": "Davis (Male US)"
            }
    
    def get_edge_voice_name(self, voice_name: str) -> str:
        """Get Microsoft Edge voice name"""
        voice_map = {
            "aria": "en-US-AriaNeural",
            "guy": "en-US-GuyNeural",
            "jenny": "en-US-JennyNeural",
            "davis": "en-US-DavisNeural"
        }
        return voice_map.get(voice_name, voice_map["aria"])