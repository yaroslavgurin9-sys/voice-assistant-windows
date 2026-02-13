import json
from vosk import Model, KaldiRecognizer
from pathlib import Path
from core.logger import app_logger, log_error
from config.settings import config

class SpeechToTextPipeline:
    """Speech to Text using Vosk"""
    
    def __init__(self):
        self.model = None
        self.recognizer = None
        self._init_model()
        app_logger.info("SpeechToTextPipeline initialized")
    
    def _init_model(self):
        """Initialize Vosk model"""
        try:
            model_path = Path(config.vosk.MODEL_PATH)
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            self.model = Model(str(model_path))
            self.recognizer = KaldiRecognizer(self.model, config.audio.SAMPLE_RATE)
            
            app_logger.info(f"Vosk model loaded from {model_path}")
            
        except Exception as e:
            log_error("SpeechToTextPipeline._init_model", e)
            raise
    
    def recognize(self, audio_data: bytes) -> str:
        """Recognize speech from audio data"""
        try:
            recognizer = KaldiRecognizer(self.model, config.audio.SAMPLE_RATE)
            
            if recognizer.AcceptWaveform(audio_data):
                result = json.loads(recognizer.Result())
            else:
                result = json.loads(recognizer.PartialResult())
            
            if 'result' in result:
                recognized_text = ' '.join([item['conf'] for item in result['result']])
                return recognized_text.lower().strip()
            elif 'partial' in result:
                return result['partial'].lower().strip()
            
            return ""
            
        except Exception as e:
            log_error("SpeechToTextPipeline.recognize", e)
            return ""
