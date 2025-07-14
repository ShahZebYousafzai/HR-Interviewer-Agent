from datetime import datetime
from langchain.schema import HumanMessage, AIMessage
from agents.base_agent import BaseAgent
from agents.profile_analyzer import ProfileAnalyzerAgent
from agents.question_bank import QuestionBankAgent
from core.types import ChatState
from utils.timer import TimerUtils
from core.exceptions import AgentError

class EnhancedChatAgent(BaseAgent):
    """Enhanced chat agent with profile awareness and voice capabilities"""

    def __init__(self, model_name: str = "llama3.2"):
        super().__init__(model_name)
        self.profile_analyzer = ProfileAnalyzerAgent(model_name)
        self.question_bank_agent = QuestionBankAgent(model_name)
        self.current_question_index = 0

    def process(self, state: ChatState) -> ChatState:
        """Process the user message and generate response"""
        try:
            # Check if interview time is up
            if self._check_time_up(state):
                return self._handle_time_up(state)
            
            # Get the last human message
            user_input = self._extract_user_input(state)
            
            # Handle different interview stages
            response = self._route_to_stage_handler(user_input, state)

            # Add AI response to messages
            state["messages"].append(AIMessage(content=response))

            # Update conversation history
            self._update_conversation_history(state, user_input, response)

            return state

        except Exception as e:
            raise AgentError(f"Chat processing failed: {e}")

    def _extract_user_input(self, state: ChatState) -> str:
        """Extract user input from messages"""
        if state["messages"]:
            last_message = state["messages"][-1]
            if isinstance(last_message, HumanMessage):
                return last_message.content
        return "Hello"

    def _update_conversation_history(self, state: ChatState, user_input: str, response: str):
        """Update conversation history"""
        state["conversation_history"].append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now().isoformat(),
        })

    def _check_time_up(self, state: ChatState) -> bool:
        """Check if interview time is up"""
        if state.get("is_interview_ended", False):
            return True
            
        start_time = state.get("interview_start_time")
        duration = state.get("interview_duration", 30)
        
        return TimerUtils.is_time_up(start_time, duration)

    def _handle_time_up(self, state: ChatState) -> ChatState:
        """Handle when interview time is up"""
        if not state.get("is_interview_ended", False):
            final_message = self._generate_time_up_message(state)
            
            state["interview_stage"] = "ended"
            state["is_interview_ended"] = True
            
            state["messages"].append(AIMessage(content=final_message))
            self._update_conversation_history(state, "Time is up", final_message)
        
        return state

    def _generate_time_up_message(self, state: ChatState) -> str:
        """Generate conclusion message when time is up"""
        profile_analysis = state.get("profile_analysis", {})
        domain = profile_analysis.get("domain", "your field")
        
        return f"""⏰ **Time's Up!**

Thank you so much for your time today. I really enjoyed learning about your experience in {domain} and your professional journey. We'll be in touch soon regarding the next steps. Have a great day!"""

    def _route_to_stage_handler(self, user_input: str, state: ChatState) -> str:
        """Route to appropriate stage handler"""
        stage = state["interview_stage"]
        
        if stage == "greeting":
            return self._handle_greeting(user_input, state)
        elif stage == "profile_collection":
            return self._handle_profile_collection(user_input, state)
        elif stage == "interview":
            return self._handle_interview(user_input, state)
        elif stage == "ended":
            return "Thank you for your time. The interview has concluded."
        else:
            return "How can I help you today?"

    def _handle_greeting(self, user_input: str, state: ChatState) -> str:
        """Handle initial greeting"""
        state["interview_start_time"] = datetime.now()
        state["interview_stage"] = "profile_collection"
        state["is_interview_ended"] = False

        return """Hello! Welcome to the interview. I'm excited to learn more about you today. 

⏰ Please note that this interview will last for the allocated time.

To get started, could you please tell me about your professional background? Include:
- Your current role or recent experience
- Key skills and technologies you work with
- What type of position interests you

This will help me tailor our conversation to your experience."""

    def _handle_profile_collection(self, user_input: str, state: ChatState) -> str:
        """Collect and analyze candidate profile"""
        
        # Store and analyze profile
        state["candidate_info"]["profile_text"] = user_input
        profile_analysis = self.profile_analyzer.process(user_input)
        state["profile_analysis"] = profile_analysis

        # Generate customized questions
        question_bank = self.question_bank_agent.process(profile_analysis)
        state["question_bank"] = question_bank
        state["interview_stage"] = "interview"
        self.current_question_index = 0

        # Provide feedback and ask first question
        domain = profile_analysis.get("domain", "your field")
        skills = ', '.join(profile_analysis.get("skills", [])[:3])
        
        feedback = f"""Thank you! I can see you have experience in {domain} with skills in {skills}. 

Now let's dive deeper into your experience. """

        if question_bank:
            first_question = question_bank[0]["question"]
            state["current_question"] = first_question
            return feedback + first_question
        else:
            return feedback + "Can you tell me about a recent project you're particularly proud of?"

    def _handle_interview(self, user_input: str, state: ChatState) -> str:
        """Handle main interview conversation"""
        
        profile_analysis = state.get("profile_analysis", {})
        question_bank = state.get("question_bank", [])
        context = self._build_interview_context(state)

        prompt = f"""You are an HR interviewer conducting a job interview. 

Candidate Profile:
- Domain: {profile_analysis.get('domain', 'General')}
- Experience Level: {profile_analysis.get('experience_level', 'Mid')}
- Key Skills: {', '.join(profile_analysis.get('skills', [])[:3])}

Recent Context:
{context}

Candidate's response: "{user_input}"

Provide a thoughtful follow-up. You can:
1. Ask a relevant follow-up question
2. Explore their skills in more depth
3. Move to the next topic

Keep your response conversational and under 3 sentences."""

        try:
            response = self.llm.invoke(prompt)

            # Optionally move to next structured question
            if (question_bank and 
                self.current_question_index < len(question_bank) - 1 and
                len(state.get("conversation_history", [])) % 3 == 0):
                
                self.current_question_index += 1
                next_q = question_bank[self.current_question_index]
                state["current_question"] = next_q["question"]
                response += f"\n\nLet me ask you about something else: {next_q['question']}"

            return response.strip()

        except Exception as e:
            raise AgentError(f"Interview response generation failed: {e}")

    def _build_interview_context(self, state: ChatState) -> str:
        """Build context from recent conversation"""
        context = ""
        conversation_history = state.get("conversation_history", [])
        if conversation_history:
            recent_history = conversation_history[-2:]
            for exchange in recent_history:
                context += f"Interviewer: {exchange['assistant']}\nCandidate: {exchange['user']}\n"
        return context