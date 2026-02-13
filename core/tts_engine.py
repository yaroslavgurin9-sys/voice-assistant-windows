import pyttsx3
import threading
from core.logger import app_logger, log_error
from config.settings import config

class TextToSpeechEngine:
    """Text to Speech using pyttsx3"""
    
    def __init__(self):
        self.engine = pyttsx3.init(driverName=config.tts.ENGINE)
        self._configure_engine()
        self.speech_lock = threading.Lock()
        
        app_logger.info("TextToSpeechEngine initialized")
    
    def _configure_engine(self):
        """Configure TTS engine"""
        try:
            self.engine.setProperty('rate', config.tts.RATE)
            self.engine.setProperty('volume', config.tts.VOLUME)
            
            voices = self.engine.getProperty('voices')
            
            ru_voice = None
            for voice in voices:
                if 'russian' in voice.languages or 'ru' in voice.languages:
                    ru_voice = voice
                    break
            
            if ru_voice:
                self.engine.setProperty('voice', ru_voice.id)
                app_logger.info(f"Russian voice set: {ru_voice.name}")
            else:
                app_logger.warning("Russian voice not found, using default")
            
        except Exception as e:
            log_error("TextToSpeechEngine._configure_engine", e)
    
    def speak(self, text: str, wait: bool = True):
        """Speak text"""
        if not text:
            return
        
        try:
            with self.speech_lock:
                app_logger.info(f"TTS: '{text}'")
                self.engine.say(text)
                
                if wait:
                    self.engine.runAndWait()
                else:
                    threading.Thread(target=self.engine.runAndWait, daemon=True).start()
                    
        except Exception as e:
            log_error("TextToSpeechEngine.speak", e)
    
    def stop(self):
        """Stop speech"""
        try:
            self.engine.stop()
            app_logger.info("TTS stopped")
        except Exception as e:
            log_error("TextToSpeechEngine.stop", e)

tts_engine = TextToSpeechEngine()
