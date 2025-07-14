from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime
from langchain.schema import BaseMessage

class ChatState(TypedDict):
    messages: List[BaseMessage]
    current_question: str
    interview_stage: str
    candidate_info: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    profile_analysis: Dict[str, Any]
    question_bank: List[Dict[str, Any]]
    interview_start_time: Optional[datetime]
    interview_duration: int
    is_interview_ended: bool
    voice_enabled: bool
    selected_voice: str

class ProfileAnalysis(TypedDict):
    experience_level: str
    skills: List[str]
    domain: str
    years_experience: int
    strengths: List[str]
    focus_areas: List[str]

class InterviewQuestion(TypedDict):
    question: str
    type: str
    difficulty: str
    category: str
    domain: Optional[str]