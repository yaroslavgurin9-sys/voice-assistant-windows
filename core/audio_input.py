import pyaudio
import numpy as np
from collections import deque
from core.logger import app_logger, log_error
from config.settings import config

class AudioCapture:
    """Handles audio capture from microphone"""
    
    def __init__(self):
        self.CHUNK = config.audio.CHUNK_SIZE
        self.FORMAT = getattr(pyaudio.paInt16, 'value', pyaudio.paInt16)
        self.CHANNELS = config.audio.CHANNELS
        self.RATE = config.audio.SAMPLE_RATE
        
        self.p = pyaudio.PyAudio()
        self.stream = None
        self._init_stream()
        
        app_logger.info(f"AudioCapture initialized: {self.RATE}Hz, {self.CHANNELS}ch, {self.CHUNK} chunk")
    
    def _init_stream(self):
        """Initialize audio stream"""
        try:
            device_index = config.audio.DEVICE_INDEX
            
            if device_index >= 0:
                device_info = self.p.get_device_info_by_index(device_index)
                app_logger.info(f"Using device: {device_info['name']}")
            
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                input_device_index=device_index if device_index >= 0 else None,
                start=False
            )
            
            self.stream.start_stream()
            app_logger.info("Audio stream started")
            
        except Exception as e:
            log_error("AudioCapture._init_stream", e)
            raise
    
    def get_audio_chunk(self, timeout=1.0):
        """Get single audio chunk"""
        try:
            if not self.stream or not self.stream.is_active():
                return None
            
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            return data
            
        except Exception as e:
            log_error("AudioCapture.get_audio_chunk", e)
            return None
    
    def stop(self):
        """Stop audio capture"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        app_logger.info("Audio capture stopped")


class VoiceActivityDetector:
    """Detects voice activity in audio stream"""
    
    def __init__(self):
        self.CHUNK = config.audio.CHUNK_SIZE
        self.RATE = config.audio.SAMPLE_RATE
        self.THRESHOLD = config.vad.ENERGY_THRESHOLD
        self.MIN_DURATION = config.vad.MIN_DURATION_MS
        
        self.buffer = deque(maxlen=int(self.RATE / self.CHUNK * 2))
        self.is_voice_active = False
        self.voice_start_time = None
        self.silence_start_time = None
        
        app_logger.info(f"VAD initialized: threshold={self.THRESHOLD}, min_duration={self.MIN_DURATION}ms")
    
    def reset(self):
        """Reset VAD state"""
        self.buffer.clear()
        self.is_voice_active = False
        self.voice_start_time = None
        self.silence_start_time = None
    
    def get_energy(self, audio_chunk):
        """Calculate energy of audio chunk"""
        try:
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            energy = np.sqrt(np.mean(audio_data.astype(float) ** 2))
            return energy
        except:
            return 0
    
    def detect_speech_start(self, audio_chunk):
        """Detect speech start (voice activity onset)"""
        energy = self.get_energy(audio_chunk)
        
        if energy > self.THRESHOLD and not self.is_voice_active:
            self.voice_start_time = 0
            self.is_voice_active = True
            app_logger.debug(f"Speech started (energy: {energy:.2f})")
            return True
        
        return False
    
    def detect_speech_end(self, audio_chunk):
        """Detect speech end (silence after voice)"""
        energy = self.get_energy(audio_chunk)
        
        if self.is_voice_active:
            if energy < self.THRESHOLD:
                if self.silence_start_time is None:
                    self.silence_start_time = 0
                else:
                    self.silence_start_time += len(audio_chunk) / self.RATE * 1000
                
                if self.silence_start_time > self.MIN_DURATION:
                    self.is_voice_active = False
                    self.silence_start_time = None
                    app_logger.debug(f"Speech ended (silence detected, energy: {energy:.2f})")
                    return True
            else:
                self.silence_start_time = None
        
        return False
    
    def is_active(self):
        """Check if voice activity is currently detected"""
        return self.is_voice_active
