from langgraph.graph import StateGraph, END
from core.types import ChatState
from agents.chat_agent import EnhancedChatAgent

def create_enhanced_chat_graph(model_name: str = "llama3.2"):
    """Create the enhanced LangGraph workflow"""
    
    chat_agent = EnhancedChatAgent(model_name)
    workflow = StateGraph(ChatState)
    
    def process_message(state: ChatState) -> ChatState:
        return chat_agent.process(state)
    
    workflow.add_node("chat", process_message)
    workflow.set_entry_point("chat")
    workflow.add_edge("chat", END)
    
    return workflow.compile()