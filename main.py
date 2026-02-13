import os
import sys
import time
import threading
import signal
from typing import Optional
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.logger import app_logger, log_error
from core.audio_input import AudioCapture, VoiceActivityDetector
from core.wake_word import WakeWordDetector
from core.stt_engine import SpeechToTextPipeline
from core.tts_engine import tts_engine
from core.command_router import CommandRouter
from config.settings import config


class VoiceAssistant:
    """Main Voice Assistant Class"""

    def __init__(self, enable_gui: bool = False):
        app_logger.info("=" * 60)
        app_logger.info("Initializing Voice Assistant...")
        app_logger.info("=" * 60)

        self.enable_gui = enable_gui and config.gui.USE_GUI
        self.is_running = False
        self.is_listening = False

        self.stt_pipeline = SpeechToTextPipeline()
        self.command_router = CommandRouter()
        self.audio_capture = AudioCapture()
        self.vad = VoiceActivityDetector()

        self.wake_word_detector = WakeWordDetector(
            on_wake=self._on_wake_word,
            on_partial_result=self._on_partial_result
        )

        self.gui = None
        if self.enable_gui:
            try:
                from ui.gui_main import VoiceAssistantGUI
                self.gui = VoiceAssistantGUI(self)
            except Exception as e:
                app_logger.warning(f"GUI initialization failed: {e}")
                self.enable_gui = False

        app_logger.info("Voice Assistant initialized successfully")

    def start(self):
        """Start the assistant"""
        if self.is_running:
            return

        self.is_running = True
        app_logger.info("Voice Assistant started")
        tts_engine.speak("Ассистент готов", wait=False)
        self.wake_word_detector.start()

        if self.gui:
            self.gui.show()
            self.gui.run()
        else:
            self._console_mode()

    def stop(self):
        """Stop the assistant"""
        if not self.is_running:
            return

        app_logger.info("Stopping Voice Assistant...")
        self.is_running = False
        self.wake_word_detector.stop()
        self.audio_capture.stop()

        if self.gui:
            self.gui.close()

        app_logger.info("Voice Assistant stopped")

    def _on_wake_word(self):
        """Wake word callback"""
        app_logger.info("WAKE WORD DETECTED - Starting command listening")
        tts_engine.speak("Слушаю", wait=False)

        self.is_listening = True
        audio_buffer = []
        self.vad.reset()
        start_time = time.time()
        timeout = config.vosk.TIMEOUT_SECONDS
        silence_count = 0

        while self.is_listening and (time.time() - start_time) < timeout:
            try:
                chunk = self.audio_capture.get_audio_chunk(timeout=0.1)
                if chunk is None:
                    continue

                audio_buffer.append(chunk)

                if self.vad.detect_speech_end(chunk):
                    silence_count += 1
                    if silence_count > 3:
                        break
                else:
                    silence_count = 0

            except Exception as e:
                log_error("VoiceAssistant._on_wake_word", e)
                break

        if audio_buffer:
            self._process_command(audio_buffer)

        self.is_listening = False
        self.vad.reset()

    def _process_command(self, audio_buffer: list):
        """Process recognized command"""
        try:
            audio_data = b''.join(audio_buffer)
            recognized_text = self.stt_pipeline.recognize(audio_data)

            if not recognized_text:
                app_logger.warning("No speech recognized")
                tts_engine.speak("Не удалось распознать речь, повторите попытку", wait=False)
                return

            app_logger.info(f"Recognized: '{recognized_text}'")
            command_type, result, success = self.command_router.route_command(recognized_text)

            if success:
                app_logger.info(f"Command executed: {command_type} -> {result}")
                tts_engine.speak(result, wait=False)
            else:
                app_logger.warning(f"Command execution failed: {result}")
                tts_engine.speak("Не удалось выполнить команду", wait=False)

        except Exception as e:
            log_error("VoiceAssistant._process_command", e)
            tts_engine.speak("Произошла ошибка при выполнении команды", wait=False)

    def _on_partial_result(self, partial_text: str):
        """Partial recognition result"""
        if self.gui:
            self.gui.update_partial_result(partial_text)

    def _console_mode(self):
        """Console mode (without GUI)"""
        app_logger.info("Running in console mode. Press Ctrl+C to exit.")
        print("\n" + "=" * 60)
        print("Voice Assistant Ready!")
        print("Say: 'Ассистент', 'Привет ассистент' or 'Окей ассистент'")
        print("Press Ctrl+C to exit")
        print("=" * 60 + "\n")

        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.stop()


def signal_handler(sig, frame):
    """Signal handler for Ctrl+C"""
    print("\n\nReceived interrupt signal. Shutting down...")
    if 'assistant' in globals():
        assistant.stop()
    sys.exit(0)


def main():
    """Main function"""
    signal.signal(signal.SIGINT, signal_handler)

    try:
        assistant = VoiceAssistant(enable_gui=config.gui.USE_GUI)
        assistant.start()
    except Exception as e:
        log_error("main", e)
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
