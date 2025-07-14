import re
from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from core.types import ProfileAnalysis, InterviewQuestion
from core.exceptions import AgentError

class QuestionBankAgent(BaseAgent):
    """Generate and manage interview questions based on profile"""

    def process(self, profile_analysis: ProfileAnalysis) -> List[InterviewQuestion]:
        """Generate customized questions based on profile analysis"""
        
        base_questions = self._get_base_questions()
        custom_questions = self._generate_custom_questions(profile_analysis)
        
        all_questions = base_questions + custom_questions
        return self._prioritize_questions(all_questions, profile_analysis)

    def _get_base_questions(self) -> List[InterviewQuestion]:
        """Get standard interview questions"""
        return [
            {
                "question": "Can you tell me about yourself and your background?",
                "type": "introduction",
                "difficulty": "easy",
                "category": "general",
            },
            {
                "question": "What interests you about this role?",
                "type": "motivation",
                "difficulty": "easy",
                "category": "general",
            },
            {
                "question": "Tell me about a challenging project you worked on.",
                "type": "experience",
                "difficulty": "medium",
                "category": "behavioral",
            },
            {
                "question": "How do you handle working under pressure?",
                "type": "behavioral",
                "difficulty": "medium",
                "category": "behavioral",
            },
        ]

    def _generate_custom_questions(self, profile_analysis: ProfileAnalysis) -> List[InterviewQuestion]:
        """Generate questions customized to the candidate's profile"""
        
        domain = profile_analysis.get("domain", "General")
        skills = profile_analysis.get("skills", [])
        experience_level = profile_analysis.get("experience_level", "Mid")

        prompt = f"""
        Generate 3-5 interview questions for a candidate with:
        - Domain: {domain}
        - Skills: {', '.join(skills)}
        - Experience Level: {experience_level}
        
        Create questions that are:
        1. Relevant to their domain and skills
        2. Appropriate for their experience level
        3. Mix of technical and behavioral questions
        
        Format each question as:
        Question: [question text]
        Type: [technical/behavioral/situational]
        Difficulty: [easy/medium/hard]
        """

        try:
            response = self.llm.invoke(prompt)
            return self._parse_custom_questions(response, profile_analysis)
        except Exception as e:
            raise AgentError(f"Custom question generation failed: {e}")

    def _parse_custom_questions(self, response: str, profile_analysis: ProfileAnalysis) -> List[InterviewQuestion]:
        """Parse generated questions into structured format"""
        questions = []
        question_blocks = re.split(r"\n\s*Question:", response)

        for block in question_blocks[1:]:
            try:
                lines = block.strip().split("\n")
                if lines:
                    question_text = lines[0].strip()
                    
                    type_match = re.search(r"Type:\s*(.+)", block, re.IGNORECASE)
                    difficulty_match = re.search(r"Difficulty:\s*(.+)", block, re.IGNORECASE)

                    questions.append({
                        "question": question_text,
                        "type": type_match.group(1).strip().lower() if type_match else "general",
                        "difficulty": difficulty_match.group(1).strip().lower() if difficulty_match else "medium",
                        "category": "custom",
                        "domain": profile_analysis.get("domain", "General"),
                    })
            except Exception as e:
                print(f"Error parsing question block: {e}")
                continue

        return questions

    def _prioritize_questions(self, questions: List[InterviewQuestion], profile_analysis: ProfileAnalysis) -> List[InterviewQuestion]:
        """Sort questions by relevance to candidate profile"""
        
        def relevance_score(question):
            score = 0
            
            # Prioritize questions matching candidate's domain
            if question.get("domain") == profile_analysis.get("domain"):
                score += 3

            # Prioritize appropriate difficulty
            exp_level = profile_analysis.get("experience_level", "Mid").lower()
            q_difficulty = question.get("difficulty", "medium").lower()

            if exp_level == "junior" and q_difficulty in ["easy", "medium"]:
                score += 2
            elif exp_level == "senior" and q_difficulty in ["medium", "hard"]:
                score += 2
            elif exp_level == "mid":
                score += 1

            # Prioritize custom questions
            if question.get("category") == "custom":
                score += 1

            return score

        return sorted(questions, key=relevance_score, reverse=True)