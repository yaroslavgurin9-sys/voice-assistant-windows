# Voice Assistant for Windows 11

AI-powered voice assistant for Windows 11 with offline speech recognition, intelligent routing, and local LLM integration. Similar to Alexa/Siri but fully free, private and customizable.

## Features

✨ **Core Capabilities**
- 🎤 Offline speech recognition (STT) via Vosk
- 🔊 Text-to-speech synthesis in Russian (pyttsx3)
- 🎯 Wake word detection ("Ассистент", "Привет ассистент", etc.)
- ⚡ Sub-1 second response time with local processing
- 🧠 AI chat integration (local Ollama or cloud API)
- 🌐 Web browser automation
- 📱 Application launcher with custom aliases
- 👁️ Screen analysis with OCR (Tesseract)
- ⌨️ Mouse and keyboard automation

## Quick Start

### Prerequisites
- Windows 11 with Python 3.10+
- Microphone
- Internet (for initial setup only)

### Installation

```bash
# Clone repository
git clone https://github.com/yaroslavgurin9-sys/voice-assistant-windows.git
cd voice-assistant-windows

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup

**1. Download Vosk Model**
```bash
# Download Russian model from https://alphacephei.com/vosk/models
# Extract to: models/vosk_models/model-ru/
```

**2. Install Tesseract OCR**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR\`
- Select Russian language during installation

**3. Setup LLM (Choose one)**

Option A: Ollama (Recommended)
```bash
# Download from https://ollama.ai/
# Run: ollama run neural-chat
```

Option B: LM Studio
- Download from https://lmstudio.ai/
- Start server at localhost:1234

### Run

```bash
# Console mode
python main.py

# Or with batch file
run.bat
```

Say: **"Ассистент"** to activate, then give commands.

## Usage Examples

```
"Ассистент" → Activates assistant
"Открой Chrome" → Launches Google Chrome
"Открой YouTube" → Opens youtube.com
"Прочитай что написано" → OCR text from active window
"Что такое Python?" → AI answers question
"Запусти PyCharm" → Launches IDE
"Закрой это окно" → Closes active window
```

## Project Structure

```
voice-assistant/
├── core/                          # Main modules
│   ├── audio_input.py            # Microphone capture
│   ├── wake_word.py              # Wake word detection
│   ├── stt_engine.py             # Speech recognition
│   ├── tts_engine.py             # Text-to-speech
│   ├── command_router.py         # Command routing
│   ├── system_controller.py      # App/system control
│   ├── screen_analyzer.py        # OCR and screenshots
│   ├── ai_chat.py                # LLM integration
│   └── logger.py                 # Logging
│
├── config/                        # Configuration
│   ├── settings.py               # Main settings
│   ├── commands.json             # Command mapping
│   ├── apps_registry.json        # App paths
│   ├── aliases.json              # Command aliases
│   └── system_prompt.txt         # LLM system prompt
│
├── models/                        # Models and data
│   ├── vosk_models/
│   │   └── model-ru/
│   └── prompts/
│
├── ui/                            # GUI (Optional)
│   ├── gui_main.py
│   └── gui_threads.py
│
├── logs/                          # Application logs
├── requirements.txt               # Dependencies
├── main.py                        # Entry point
├── run.bat                        # Quick launcher
└── README.md
```

## Configuration

### config/settings.py

```python
# Audio configuration
config.audio.SAMPLE_RATE = 16000
config.audio.CHUNK_SIZE = 4096

# Vosk STT
config.vosk.MODEL_PATH = "models/vosk_models/model-ru"
config.vosk.TIMEOUT_SECONDS = 30.0

# TTS
config.tts.RATE = 150  # Words per minute
config.tts.VOLUME = 0.9

# Wake words
config.wake_word.WAKE_WORDS = ["ассистент", "привет ассистент", "окей ассистент"]

# AI Settings
config.ai.USE_LOCAL_MODEL = True
config.ai.LOCAL_MODEL_TYPE = "ollama"
config.ai.OLLAMA_MODEL = "neural-chat"
config.ai.OLLAMA_API_URL = "http://localhost:11434/api/generate"
```

### Custom Commands

Edit `config/commands.json` to add command mappings:

```json
{
  "app_launcher": {
    "keywords": ["открой", "запусти"],
    "apps": [
      {"name": "chrome", "aliases": ["хром", "браузер"]}
    ]
  }
}
```

## Architecture

```
Audio Input (Microphone)
        ↓
Wake Word Detector ("Ассистент")
        ↓
Speech Recognition (Vosk STT)
        ↓
Command Router (Pattern Matching)
        ↓
┌───────┴────────┬─────────────┐
│                │             │
▼                ▼             ▼
System          Screen        AI Chat
Controller      Analyzer      Module
(Apps/Web)      (OCR/Click)    (LLM)
        │                │             │
        └────────┬───────┴─────────────┘
                 │
                 ▼
        Text-to-Speech (pyttsx3)
                 │
                 ▼
        Speaker/Audio Output
```

## Technology Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| STT | Vosk | Offline, Russian support |
| TTS | pyttsx3 | Offline, local voices |
| LLM | Ollama/LM Studio | Local or cloud API |
| OCR | Tesseract | Open source |
| Audio | sounddevice | Cross-platform |
| Automation | pyautogui | Screen/keyboard control |
| GUI | PyQt6 | Optional |
| Framework | Python 3.10+ | Async/threading |

## Troubleshooting

### Vosk model not found
```
→ Download from https://alphacephei.com/vosk/models
→ Extract model-ru to models/vosk_models/model-ru/
```

### PyAudio won't install
```bash
pip install pipwin
pipwin install pyaudio
```

### Microphone not working
```python
import sounddevice as sd
print(sd.query_devices())  # Find your device index
# Update config.audio.MIC_DEVICE_INDEX
```

### LLM not responding
- Check Ollama is running: `ollama run neural-chat`
- Verify API at http://localhost:11434/api/tags
- Check config.ai.OLLAMA_API_URL

### Tesseract not found
```
→ Install to C:\Program Files\Tesseract-OCR\
→ Update config.screen.TESSERACT_PATH
```

## Performance Optimization

- **Wake word detection**: Always-on, low CPU usage
- **STT latency**: <500ms with local Vosk
- **Command execution**: Threaded to avoid blocking
- **LLM response**: Async streaming for smooth UX
- **Logging**: Async file I/O

## Security & Privacy

✅ All processing is local (no cloud required)
✅ No data sent to external services by default
✅ Custom LLM models can be run completely offline
✅ Supports encrypted API keys for optional cloud services

## Extending

### Add New Command

```python
# In core/command_router.py
def _handle_custom_action(self, text: str) -> str:
    if 'take screenshot' in text:
        self.screen_analyzer.take_screenshot('screenshot.png')
        return "Screenshot saved"
    return "Unknown command"
```

### Add Application

Edit `config/apps_registry.json`:
```json
{
  "telegram": "C:\\Users\\Name\\AppData\\Local\\Telegram\\Telegram.exe"
}
```

### Add Wake Word

Edit `config/settings.py`:
```python
config.wake_word.WAKE_WORDS = [
    "ассистент",
    "привет ассистент",
    "окей ассистент",
    "привет",  # New wake word
]
```

## Logging

Logs are saved to `logs/assistant.log` with:
- Timestamp
- Recognized text
- Command type
- Execution result

```python
from core.logger import app_logger
app_logger.info("Custom message")
```

## Advanced Usage

### Remote API Integration

```python
# Use cloud API instead of local LLM
config.ai.USE_LOCAL_MODEL = False
config.ai.USE_CLOUD_API = True
config.ai.CLOUD_API_TYPE = "openai"
config.ai.CLOUD_API_KEY = "sk-..."
```

### Multiple LLM Models

```python
# Switch between models
config.ai.OLLAMA_MODEL = "mistral"  # Fast
config.ai.OLLAMA_MODEL = "neural-chat"  # Better quality
```

### Enable GUI

```python
# In main.py
assistant = VoiceAssistant(enable_gui=True)
assistant.start()
```

## Contributing

Feel free to fork, modify, and submit pull requests!

## License

MIT License - Free for personal and commercial use

## Author

Created as a comprehensive voice assistant framework for Windows 11.

## Support

For issues, questions, or suggestions:
1. Check existing issues on GitHub
2. Review logs in `logs/assistant.log`
3. Open a new issue with:
   - Windows version
   - Python version
   - Error logs
   - Reproduction steps

## Roadmap

- [ ] GUI dashboard with command history
- [ ] Global hotkeys for quick access
- [ ] Multi-language support (English, Spanish, etc.)
- [ ] Skill plugins system
- [ ] Database for persistent context
- [ ] Integration with weather/news APIs
- [ ] Desktop notifications
- [ ] Command scheduling
- [ ] Voice recording and playback
- [ ] Advanced NLP for better intent detection

---

**Status**: Active Development
**Last Updated**: February 2026
**Python**: 3.10+
**OS**: Windows 11
