import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)


@dataclass
class AudioConfig:
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 4096
    CHANNELS: int = 1
    FORMAT: str = "int16"
    MIC_DEVICE_INDEX: Optional[int] = None
    THRESHOLD_SILENCE: int = 500


@dataclass
class VoskConfig:
    MODEL_PATH: str = str(MODELS_DIR / "vosk_models" / "model-ru")
    SAMPLE_RATE: int = 16000
    TIMEOUT_SECONDS: float = 30.0
    CONFIDENCE_THRESHOLD: float = 0.5


@dataclass
class TTSConfig:
    RATE: int = 150
    VOLUME: float = 0.9
    VOICE_INDEX: int = 1


@dataclass
class WakeWordConfig:
    WAKE_WORDS: List[str] = None
    SENSITIVITY: float = 0.5
    CONTINUOUS_LISTENING: bool = True

    def __post_init__(self):
        if self.WAKE_WORDS is None:
            self.WAKE_WORDS = ["ассистент", "привет ассистент", "окей ассистент"]


@dataclass
class AIConfig:
    USE_LOCAL_MODEL: bool = True
    LOCAL_MODEL_TYPE: str = "ollama"
    OLLAMA_API_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MODEL: str = "neural-chat"
    USE_CLOUD_API: bool = False
    CLOUD_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CLOUD_API_TYPE: str = "openai"
    MAX_TOKENS: int = 256
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    TIMEOUT: int = 30
    SYSTEM_PROMPT_PATH: str = str(CONFIG_DIR / "system_prompt.txt")


@dataclass
class CommandConfig:
    COMMANDS_JSON: str = str(CONFIG_DIR / "commands.json")
    APPS_REGISTRY_JSON: str = str(CONFIG_DIR / "apps_registry.json")
    ALIASES_JSON: str = str(CONFIG_DIR / "aliases.json")


@dataclass
class ScreenAnalyzerConfig:
    USE_TESSERACT: bool = True
    TESSERACT_PATH: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    SCREENSHOT_QUALITY: int = 95
    AUTO_LANGUAGE: str = "rus"


@dataclass
class LoggingConfig:
    LOG_FILE: str = str(LOGS_DIR / "assistant.log")
    ERROR_LOG_FILE: str = str(LOGS_DIR / "errors.log")
    LOG_LEVEL: str = "INFO"
    MAX_LOG_SIZE: int = 10 * 1024 * 1024
    BACKUP_COUNT: int = 5


@dataclass
class GUIConfig:
    USE_GUI: bool = True
    THEME: str = "dark"
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    SHOW_ON_STARTUP: bool = True


class Config:
    def __init__(self):
        self.audio = AudioConfig()
        self.vosk = VoskConfig()
        self.tts = TTSConfig()
        self.wake_word = WakeWordConfig()
        self.ai = AIConfig()
        self.command = CommandConfig()
        self.screen = ScreenAnalyzerConfig()
        self.logging = LoggingConfig()
        self.gui = GUIConfig()
        self._check_vosk_model()

    def _check_vosk_model(self):
        model_path = Path(self.vosk.MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found: {self.vosk.MODEL_PATH}\n"
                f"Download from https://alphacephei.com/vosk/models"
            )

    @staticmethod
    def load_json(path: str) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_json(path: str, data: Dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


config = Config()
