class InterviewSystemError(Exception):
    """Base exception for interview system"""
    pass

class AudioError(InterviewSystemError):
    """Audio-related errors"""
    pass

class TTSError(AudioError):
    """Text-to-Speech errors"""
    pass

class STTError(AudioError):
    """Speech-to-Text errors"""
    pass

class ModelError(InterviewSystemError):
    """LLM model errors"""
    pass

class AgentError(InterviewSystemError):
    """Agent-related errors"""
    pass