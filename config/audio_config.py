from dataclasses import dataclass
from typing import Dict

@dataclass
class AudioConfig:
    """Audio configuration settings for ElevenLabs"""
    
    VOICE_OPTIONS: Dict[str, str] = None
    DEFAULT_VOICE: str = "rachel"
    DEFAULT_SPEED: float = 1.0
    MIN_SPEED: float = 0.5
    MAX_SPEED: float = 2.0
    
    def __post_init__(self):
        if self.VOICE_OPTIONS is None:
            # ElevenLabs voice options with their display names
            self.VOICE_OPTIONS = {
                "rachel": "Rachel (Female, Calm)",
                "domi": "Domi (Female, Strong)",
                "bella": "Bella (Female, Soft)",
                "elli": "Elli (Female, Emotional)",
                "josh": "Josh (Male, Deep)",
                "arnold": "Arnold (Male, Crisp)",
                "adam": "Adam (Male, Deep)",
                "sam": "Sam (Male, Raspy)"
            }
    
    def get_elevenlabs_voice_id(self, voice_name: str) -> str:
        """Get ElevenLabs voice ID from voice name"""
        voice_map = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",
            "domi": "AZnzlk1XvdvUeBnXmlld", 
            "bella": "EXAVITQu4vr4xnSDxMaL",
            "elli": "MF3mGyEYCl7XYWbV9V6O",
            "josh": "TxGEqnHWrfWFTfGW9XjX",
            "arnold": "VR6AewLTigWG4xSOukaG",
            "adam": "pNInz6obpgDQGcFmaJgB",
            "sam": "yoZ06aMxZJJ28mfd3POQ"
        }
        return voice_map.get(voice_name, voice_map["rachel"])
    
    def get_voice_settings(self, voice_name: str) -> Dict[str, float]:
        """Get optimized settings for each voice"""
        settings_map = {
            "rachel": {"stability": 0.75, "similarity_boost": 0.75, "style": 0.0},
            "domi": {"stability": 0.70, "similarity_boost": 0.80, "style": 0.2},
            "bella": {"stability": 0.80, "similarity_boost": 0.70, "style": 0.1},
            "elli": {"stability": 0.65, "similarity_boost": 0.75, "style": 0.3},
            "josh": {"stability": 0.75, "similarity_boost": 0.85, "style": 0.1},
            "arnold": {"stability": 0.80, "similarity_boost": 0.80, "style": 0.0},
            "adam": {"stability": 0.70, "similarity_boost": 0.85, "style": 0.2},
            "sam": {"stability": 0.65, "similarity_boost": 0.75, "style": 0.4}
        }
        return settings_map.get(voice_name, settings_map["rachel"])