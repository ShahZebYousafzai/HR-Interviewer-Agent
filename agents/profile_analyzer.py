from typing import Dict, Any
from agents.base_agent import BaseAgent
from core.types import ProfileAnalysis
from utils.text_processing import TextProcessor
from core.exceptions import AgentError

class ProfileAnalyzerAgent(BaseAgent):
    """Analyze candidate profile and extract key information"""

    def __init__(self, model_name: str = "llama3.2"):
        super().__init__(model_name)
        self.text_processor = TextProcessor()

    def process(self, profile_text: str) -> ProfileAnalysis:
        """Analyze candidate profile text and extract structured information"""
        
        prompt = self._build_analysis_prompt(profile_text)
        
        try:
            response = self.llm.invoke(prompt)
            return self.text_processor.parse_profile_response(response)
        except Exception as e:
            raise AgentError(f"Profile analysis failed: {e}")

    def _build_analysis_prompt(self, profile_text: str) -> str:
        """Build the analysis prompt"""
        return f"""
        Analyze the following candidate profile and extract key information:

        Profile: "{profile_text}"

        Extract and format the following information:
        1. Experience Level (Junior/Mid/Senior)
        2. Primary Skills (list up to 5 main skills)
        3. Domain/Field (e.g., Software Engineering, Data Science, Marketing)
        4. Years of Experience (estimate if not explicitly stated)
        5. Key Strengths (based on description)
        6. Potential Interview Focus Areas

        Format your response as:
        Experience Level: [level]
        Primary Skills: [skill1, skill2, skill3]
        Domain: [domain]
        Years of Experience: [number]
        Key Strengths: [strength1, strength2]
        Interview Focus: [area1, area2, area3]
        """

    def get_default_profile(self) -> ProfileAnalysis:
        """Return default profile when analysis fails"""
        return {
            "experience_level": "Mid",
            "skills": ["Communication", "Problem Solving"],
            "domain": "General",
            "years_experience": 3,
            "strengths": ["Adaptable", "Team Player"],
            "focus_areas": ["General Experience", "Problem Solving"],
        }