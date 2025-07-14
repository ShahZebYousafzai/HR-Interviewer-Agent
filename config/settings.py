from dataclasses import dataclass
from typing import Dict, Any
import os

class ModelConfig:
    """Model configuration settings"""
    model_name: str = "llama3.2"
    temperature: float = 0.7
    num_ctx: int = 4096
    num_predict: int = 512

class InterviewConfig:
    """Interview configuration settings"""
    default_duration: int = 30
    min_duration: int = 5
    max_duration: int = 120
    warning_threshold: int = 300  # 5 minutes in seconds

class AppConfig:
    """Main application configuration"""
    page_title: str = "HR Interview System"
    page_icon: str = "🎯"
    layout: str = "wide"
    
    # Environment
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Model settings
    model: ModelConfig = ModelConfig()
    
    # Interview settings
    interview: InterviewConfig = InterviewConfig()

# Global configuration instance
CONFIG = AppConfig()