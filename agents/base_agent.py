from abc import ABC, abstractmethod
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from core.exceptions import ModelError

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model_name: str = "llama3.2"):
        self.llm = self._initialize_llm(model_name)
    
    def _initialize_llm(self, model_name: str):
        """Initialize the local LLAMA model via Ollama"""
        try:
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            
            llm = Ollama(
                model=model_name,
                callback_manager=callback_manager,
                temperature=0.7,
                num_ctx=4096,
                num_predict=512,
            )
            
            # Test the model
            test_response = llm.invoke("Hello")
            print(f"✅ Local LLM initialized successfully with model: {model_name}")
            return llm
            
        except Exception as e:
            raise ModelError(f"Error initializing local LLM: {e}")
    
    @abstractmethod
    def process(self, *args, **kwargs):
        """Process method to be implemented by subclasses"""
        pass