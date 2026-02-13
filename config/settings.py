import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass, field

load_dotenv()

@dataclass
class AudioConfig:
    CHUNK_SIZE: int = int(os.getenv('AUDIO_CHUNK_SIZE', 4096))
    CHANNELS: int = int(os.getenv('AUDIO_CHANNELS', 1))
    SAMPLE_RATE: int = int(os.getenv('AUDIO_SAMPLE_RATE', 16000))
    DEVICE_INDEX: int = int(os.getenv('AUDIO_DEVICE_INDEX', -1))

@dataclass
class VoskConfig:
    MODEL_PATH: str = os.getenv('VOSK_MODEL_PATH', './models/vosk_models/vosk-model-ru-0.42-big')
    TIMEOUT_SECONDS: int = int(os.getenv('VOSK_TIMEOUT_SECONDS', 10))

@dataclass
class TTSConfig:
    RATE: int = int(os.getenv('TTS_RATE', 150))
    VOLUME: float = float(os.getenv('TTS_VOLUME', 0.9))
    ENGINE: str = os.getenv('TTS_ENGINE', 'sapi5')

@dataclass
class VADConfig:
    ENERGY_THRESHOLD: int = int(os.getenv('VAD_ENERGY_THRESHOLD', 1000))
    MIN_DURATION_MS: int = int(os.getenv('VAD_MIN_DURATION_MS', 500))

@dataclass
class GUIConfig:
    USE_GUI: bool = os.getenv('GUI_USE_GUI', 'False').lower() == 'true'
    THEME: str = os.getenv('GUI_THEME', 'dark')

@dataclass
class LoggingConfig:
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', './logs/voice_assistant.log')
    ERROR_LOG_FILE: str = os.getenv('ERROR_LOG_FILE', './logs/errors.log')
    MAX_LOG_SIZE: int = int(os.getenv('MAX_LOG_SIZE', 5242880))
    BACKUP_COUNT: int = int(os.getenv('BACKUP_COUNT', 3))

@dataclass
class Config:
    audio: AudioConfig = field(default_factory=AudioConfig)
    vosk: VoskConfig = field(default_factory=VoskConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    vad: VADConfig = field(default_factory=VADConfig)
    gui: GUIConfig = field(default_factory=GUIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

config = Config()

if __name__ == '__main__':
    print("Configuration loaded:")
    print(f"Audio: chunk={config.audio.CHUNK_SIZE}, rate={config.audio.SAMPLE_RATE}Hz")
    print(f"Vosk: model={config.vosk.MODEL_PATH}")
    print(f"TTS: rate={config.tts.RATE}, volume={config.tts.VOLUME}")
    print(f"Logging: level={config.logging.LOG_LEVEL}, file={config.logging.LOG_FILE}")
