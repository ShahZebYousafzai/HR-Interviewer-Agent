# HR Interview System 🎯

An AI-powered interview system that conducts intelligent, voice-enabled interviews using Llama3.2 and advanced speech technologies.

## 🌟 Features

### Core Capabilities
- **AI-Powered Interviews**: Leverages Llama3.2 via Ollama for intelligent conversation flow
- **Voice Interaction**: Full voice support with Text-to-Speech (Edge TTS) and Speech-to-Text (Google)
- **Profile Analysis**: Automatically analyzes candidate profiles and tailors questions
- **Dynamic Question Generation**: Creates customized questions based on candidate background
- **Real-time Timer**: Interview duration management with visual countdown
- **Conversation History**: Complete chat history with timestamps

### Technical Features
- **Local LLM**: Uses Ollama with Llama3.2 for privacy and control
- **Agent-Based Architecture**: Modular design with specialized agents for different tasks
- **LangGraph Workflow**: Structured conversation flow management
- **Streamlit UI**: Clean, interactive web interface
- **Audio Processing**: High-quality voice synthesis and recognition

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   LangGraph     │    │  Local LLM      │
│   Components    │◄──►│   Workflow      │◄──►│  (Llama3.2)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Audio System  │    │   Agent Layer   │    │  Core Services  │
│   TTS/STT       │    │   Specialized   │    │  Types/Utils    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Agent Hierarchy
- **BaseAgent**: Abstract base class for all agents
- **EnhancedChatAgent**: Main interview conductor
- **ProfileAnalyzerAgent**: Candidate profile analysis
- **QuestionBankAgent**: Dynamic question generation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Microphone access for voice features

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShahZebYousafzai/HR-Interviewer-Agent.git
   cd HR-Interviewer-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Ollama**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull Llama3.2 model
   ollama pull llama3.2
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the interface**
   Open your browser to `http://localhost:8501`

## 🎮 Usage

### Starting an Interview

1. **Configure Settings**
   - Set interview duration (5-120 minutes)
   - Enable/disable voice features
   - Select TTS voice and speed

2. **Begin Interview**
   - System starts with greeting stage
   - Candidate provides background information
   - AI analyzes profile and generates custom questions

3. **Interview Flow**
   - Dynamic conversation based on candidate responses
   - Voice input/output support
   - Real-time timer tracking
   - Automatic conclusion when time expires

### Voice Features

- **Text-to-Speech**: Microsoft Edge TTS with multiple voice options
- **Speech-to-Text**: Google Speech Recognition for voice input
- **Audio Controls**: Adjustable speech speed and voice selection

## 🔧 Configuration

### Model Configuration
```python
# config/settings.py
class ModelConfig:
    model_name: str = "llama3.2"
    temperature: float = 0.7
    num_ctx: int = 4096
    num_predict: int = 512
```

### Interview Settings
```python
class InterviewConfig:
    default_duration: int = 30
    min_duration: int = 5
    max_duration: int = 120
    warning_threshold: int = 300  # 5 minutes
```

### Audio Configuration
```python
# Available TTS voices
VOICE_OPTIONS = {
    "aria": "Aria (Female US)",
    "guy": "Guy (Male US)", 
    "jenny": "Jenny (Female US)",
    "davis": "Davis (Male US)"
}
```

## 🔄 Interview Workflow

1. **Greeting Stage**
   - Welcome message
   - Timer initialization
   - Transition to profile collection

2. **Profile Collection**
   - Gather candidate background
   - Analyze skills and experience
   - Generate custom question bank

3. **Interview Stage**
   - Dynamic questioning based on profile
   - Follow-up questions
   - Contextual conversation flow

4. **Conclusion**
   - Automatic end when timer expires
   - Summary and next steps

## 🔍 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Check if model is available
   ollama list
   ```

2. **Audio Permissions**
   - Grant microphone access to your browser
   - Check system audio settings

3. **TTS Not Working**
   - Verify internet connection for Edge TTS
   - Check audio output settings

4. **Model Loading Issues**
   ```bash
   # Reinstall model
   ollama pull llama3.2
   
   # Check Ollama status
   ollama ps
   ```

### Debug Mode

Enable debug mode in `config/settings.py`:
```python
debug: bool = True
```

*Built with ❤️ for intelligent interview experiences*