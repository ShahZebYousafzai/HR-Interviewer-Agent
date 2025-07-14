import re
from typing import Dict

class TextProcessor:
    """Text processing utilities"""
    
    @staticmethod
    def clean_text_for_speech(text: str) -> str:
        """Clean text for better speech synthesis"""
        # Remove markdown formatting
        clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text)
        clean_text = re.sub(r'#{1,6}\s*(.*)', r'\1', clean_text)
        clean_text = re.sub(r'\[.*?\]', '', clean_text)
        
        # Replace emojis with text
        emoji_replacements = {
            '⏰': 'Timer:',
            '📋': '',
            '🎯': '',
            '✅': '',
            '🔊': '',
            '🎤': ''
        }
        for emoji, replacement in emoji_replacements.items():
            clean_text = clean_text.replace(emoji, replacement)
        
        # Add natural pauses
        clean_text = re.sub(r'\.', '. ', clean_text)
        clean_text = re.sub(r'\!', '! ', clean_text)
        clean_text = re.sub(r'\?', '? ', clean_text)
        
        # Clean up multiple spaces
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text
    
    @staticmethod
    def parse_profile_response(response: str) -> Dict[str, any]:
        """Parse LLM profile analysis response"""
        analysis = {}
        
        # Extract using regex patterns
        patterns = {
            "experience_level": r"Experience Level:\s*(.+)",
            "domain": r"Domain:\s*(.+)",
            "years_experience": r"Years of Experience:\s*(\d+)",
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if key == "years_experience":
                analysis[key] = int(match.group(1)) if match else 3
            else:
                analysis[key] = match.group(1).strip() if match else ("Mid" if key == "experience_level" else "General")

        # Extract lists
        list_patterns = {
            "skills": r"Primary Skills:\s*(.+)",
            "strengths": r"Key Strengths:\s*(.+)",
            "focus_areas": r"Interview Focus:\s*(.+)"
        }
        
        for key, pattern in list_patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                items_text = match.group(1).strip()
                analysis[key] = [item.strip() for item in items_text.split(",")]
            else:
                analysis[key] = []

        return analysis
