import threading
import json
from pathlib import Path
from typing import Callable, Optional
from vosk import Model, KaldiRecognizer
from core.logger import app_logger, log_error
from core.audio_input import AudioCapture
from config.settings import config

class WakeWordDetector:
    """Detects wake words using Vosk speech recognition"""
    
    WAKE_WORDS = [
        "ассистент",
        "привет ассистент",
        "окей ассистент"
    ]
    
    def __init__(self, on_wake: Callable, on_partial_result: Callable = None):
        self.on_wake = on_wake
        self.on_partial_result = on_partial_result
        self.is_running = False
        self.detection_thread = None
        
        self.audio_capture = AudioCapture()
        self._init_recognizer()
        
        app_logger.info("WakeWordDetector initialized")
    
    def _init_recognizer(self):
        """Initialize Vosk recognizer"""
        try:
            model_path = Path(config.vosk.MODEL_PATH)
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            self.model = Model(str(model_path))
            self.recognizer = KaldiRecognizer(self.model, config.audio.SAMPLE_RATE)
            self.recognizer.SetWords(self.WAKE_WORDS)
            
            app_logger.info(f"Vosk model loaded from {model_path}")
            app_logger.info(f"Wake words: {', '.join(self.WAKE_WORDS)}")
            
        except Exception as e:
            log_error("WakeWordDetector._init_recognizer", e)
            raise
    
    def start(self):
        """Start wake word detection"""
        if self.is_running:
            return
        
        self.is_running = True
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()
        app_logger.info("Wake word detection started")
    
    def stop(self):
        """Stop wake word detection"""
        self.is_running = False
        if self.detection_thread:
            self.detection_thread.join(timeout=2.0)
        self.audio_capture.stop()
        app_logger.info("Wake word detection stopped")
    
    def _detection_loop(self):
        """Main detection loop"""
        while self.is_running:
            try:
                chunk = self.audio_capture.get_audio_chunk(timeout=0.5)
                
                if chunk is None:
                    continue
                
                if self.recognizer.AcceptWaveform(chunk):
                    result = json.loads(self.recognizer.Result())
                    self._process_result(result)
                else:
                    partial = json.loads(self.recognizer.PartialResult())
                    self._process_partial(partial)
                    
            except Exception as e:
                log_error("WakeWordDetector._detection_loop", e)
    
    def _process_result(self, result: dict):
        """Process final recognition result"""
        if 'result' in result:
            recognized_text = ' '.join([item['conf'] for item in result['result']])
        elif 'partial' in result:
            recognized_text = result['partial']
        else:
            return
        
        recognized_text = recognized_text.lower().strip()
        
        for wake_word in self.WAKE_WORDS:
            if wake_word in recognized_text:
                app_logger.info(f"Wake word detected: '{wake_word}'")
                self.on_wake()
                self.recognizer.Reset()
                return
    
    def _process_partial(self, partial: dict):
        """Process partial recognition result"""
        if 'partial' in partial and self.on_partial_result:
            self.on_partial_result(partial['partial'])
