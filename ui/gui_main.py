import tkinter as tk
from tkinter import ttk
import threading
import time
import numpy as np
import pyaudio
from typing import Callable
from core.logger import app_logger

class VoiceAssistantGUI:
    """Enhanced GUI for Voice Assistant with real-time visualization"""
    
    def __init__(self, assistant, audio_callback: Callable[[bytes], None] = None):
        self.assistant = assistant
        self.audio_callback = audio_callback
        self.root = tk.Tk()
        self.root.title("🤖 Voice Assistant - Enhanced Interface")
        self.root.geometry("900x700")
        self.root.configure(bg='#0f1419')
        self.root.resizable(True, True)
        
        # Real-time data
        self.audio_data = np.zeros(100)
        self.max_level = 0
        self.is_listening = False
        self.recognized_text = ""
        self.command_status = "Ready"
        self.partial_text = ""
        
        self.canvas = None
        self.status_var = tk.StringVar(value="Готов к работе")
        self.partial_var = tk.StringVar(value="Ожидание...")
        self.command_var = tk.StringVar(value="Статус команды")
        
        self._setup_ui()
        self._start_visualization_loop()
        
        app_logger.info("Enhanced GUI initialized")
    
    def _setup_ui(self):
        """Enhanced UI layout"""
        
        # Title bar
        title_frame = tk.Frame(self.root, bg='#1a1f26', height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🤖 Voice Assistant", font=('Segoe UI', 20, 'bold'), 
                bg='#1a1f26', fg='#00d4ff').pack(side=tk.LEFT, pady=10)
        
        # Status indicator
        self.status_indicator = tk.Label(title_frame, text="●", font=('Arial', 24), 
                                       bg='#1a1f26', fg='#00ff88')
        self.status_indicator.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#0f1419')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Row 1: Audio Visualization
        viz_frame = tk.LabelFrame(main_frame, text="📊 Аудио визуализация (VU Meter)", 
                                 font=('Segoe UI', 12, 'bold'), bg='#1a1f26', fg='#ffffff', 
                                 padx=10, pady=5)
        viz_frame.pack(fill=tk.X, pady=5)
        
        self.canvas = tk.Canvas(viz_frame, width=800, height=80, bg='#0f1419', highlightthickness=0)
        self.canvas.pack(pady=5)
        
        # Row 2: Status & Partial Recognition
        status_frame = tk.LabelFrame(main_frame, text="🎤 Статус распознавания", 
                                    font=('Segoe UI', 12, 'bold'), bg='#1a1f26', fg='#ffffff',
                                    padx=10, pady=5)
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(status_frame, textvariable=self.status_var, font=('Segoe UI', 14), 
                bg='#1a1f26', fg='#00ff88').pack(anchor=tk.W)
        tk.Label(status_frame, textvariable=self.partial_var, font=('Segoe UI', 12, 'italic'), 
                bg='#1a1f26', fg='#ffaa00').pack(anchor=tk.W, pady=(0,10))
        
        # Row 3: Recognized Text & Commands
        text_frame = tk.LabelFrame(main_frame, text="💬 Распознанный текст", 
                                  font=('Segoe UI', 12, 'bold'), bg='#1a1f26', fg='#ffffff',
                                  padx=10, pady=5)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.text_display = tk.Text(text_frame, height=8, bg='#2d3748', fg='#e2e8f0',
                                   font=('Consolas', 11), state=tk.DISABLED,
                                   wrap=tk.WORD, insertbackground='#00d4ff')
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_display.yview)
        self.text_display.config(yscrollcommand=scrollbar.set)
        
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Row 4: Command Status & Logs
        cmd_frame = tk.LabelFrame(main_frame, text="⚙️ Статус выполнения", 
                                 font=('Segoe UI', 12, 'bold'), bg='#1a1f26', fg='#ffffff',
                                 padx=10, pady=5)
        cmd_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(cmd_frame, textvariable=self.command_var, font=('Segoe UI', 13, 'bold'), 
                bg='#1a1f26', fg='#00ff88').pack(anchor=tk.W)
        
        # Control buttons
        btn_frame = tk.Frame(main_frame, bg='#0f1419')
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="▶️ Запуск", command=self._on_start,
                                 width=12, height=2, bg='#10b981', fg='white',
                                 font=('Segoe UI', 11, 'bold'), relief=tk.FLAT)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ Стоп", command=self._on_stop,
                                width=12, height=2, bg='#ef4444', fg='white',
                                font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ Очистить", command=self._on_clear,
                            width=12, height=2, bg='#6b7280', fg='white',
                            font=('Segoe UI', 11, 'bold'), relief=tk.FLAT)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        self.mic_btn = tk.Button(btn_frame, text="🎤 Микрофон", command=self._toggle_mic_test,
                               width=12, height=2, bg='#3b82f6', fg='white',
                               font=('Segoe UI', 11, 'bold'), relief=tk.FLAT)
        self.mic_btn.pack(side=tk.LEFT, padx=10)
    
    def _draw_vu_meter(self, data: np.ndarray):
        """Draw real-time VU meter"""
        self.canvas.delete('all')
        
        # Normalize data
        levels = np.abs(data)
        max_val = np.max(levels) if len(levels) > 0 else 0
        self.max_level = max(self.max_level * 0.95, max_val)  # Decay
        
        bar_width = 6
        bar_gap = 2
        num_bars = 40
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 10:
            return
        
        bar_w = (width - (num_bars - 1) * bar_gap) / num_bars
        
        for i in range(num_bars):
            idx = i * len(data) // num_bars
            level = levels[idx] if idx < len(levels) else 0
            bar_height = int((level / self.max_level) * height * 0.8)
            
            # Color based on level
            if bar_height > height * 0.7:
                color = '#ef4444'  # Red
            elif bar_height > height * 0.4:
                color = '#f59e0b'  # Yellow
            else:
                color = '#10b981'  # Green
            
            x1 = i * (bar_width + bar_gap)
            y1 = height - bar_height
            x2 = x1 + bar_width
            y2 = height
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
        # Peak indicator
        peak_x = int((max_val / self.max_level) * width)
        self.canvas.create_line(peak_x, 0, peak_x, 10, fill='#fbbf24', width=3)
    
    def update_audio_level(self, audio_chunk: bytes):
        """Update audio visualization from callback"""
        if self.audio_callback:
            self.audio_callback(audio_chunk)
        try:
            data = np.frombuffer(audio_chunk, dtype=np.int16)
            self.audio_data = np.roll(self.audio_data, -len(data)//2)
            self.audio_data[-len(data)//2:] = data.astype(float) / 32768.0
            self.root.after(0, lambda: self._draw_vu_meter(self.audio_data))
        except:
            pass
    
    def update_status(self, status: str, color: str = '#00ff88'):
        """Update status display"""
        self.status_var.set(status)
        self.status_indicator.config(fg=color)
    
    def update_partial_result(self, partial_text: str):
        """Update partial recognition"""
        self.partial_var.set(f"Частичное: {partial_text or '...'}")
        self.partial_text = partial_text
    
    def update_recognized_text(self, text: str):
        """Log recognized text"""
        timestamp = time.strftime('%H:%M:%S')
        self._log_message(f"[{timestamp}] 🎤 Распознано: '{text}'")
    
    def update_command_status(self, command: str, result: str, success: bool):
        """Update command execution status"""
        status = f"Выполняю: {command} → {result}"
        color = '#00ff88' if success else '#ef4444'
        self.command_var.set(status)
        self.root.after(3000, lambda: self.command_var.set('Готов к новой команде'))  # Auto-clear
    
    def _log_message(self, message: str):
        """Add to text display with timestamp"""
        self.text_display.config(state=tk.NORMAL)
        timestamp = time.strftime('%H:%M:%S')
        self.text_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_display.see(tk.END)
        self.text_display.config(state=tk.DISABLED)
    
    def _start_visualization_loop(self):
        """Continuous visualization update"""
        self.root.after(50, self._visualization_update)
    
    def _visualization_update(self):
        """Update visualization every 50ms"""
        if self.canvas:
            self._draw_vu_meter(self.audio_data)
        self.root.after(50, self._visualization_update)
    
    def _on_start(self):
        """Start assistant"""
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.update_status("🎤 Слушаю wake-word...", '#ffaa00')
        self.assistant.start()
    
    def _on_stop(self):
        """Stop assistant"""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("⏹️ Остановлен", '#ef4444')
        self.assistant.stop()
    
    def _on_clear(self):
        """Clear logs"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)
        self.partial_var.set("Ожидание...")
        self.command_var.set("Готов к новой команде")
    
    def _toggle_mic_test(self):
        """Test microphone levels"""
        if hasattr(self, '_mic_thread') and self._mic_thread.is_alive():
            self.mic_btn.config(text="🎤 Микрофон", bg='#3b82f6')
            return
        
        def mic_test():
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                          input=True, frames_per_buffer=1024)
            self.mic_btn.config(text="🔴 Тест", bg='#ef4444')
            
            for _ in range(100):
                data = stream.read(1024)
                self.update_audio_level(data)
                time.sleep(0.05)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.root.after(0, lambda: self.mic_btn.config(text="🎤 Микрофон", bg='#3b82f6'))
        
        self._mic_thread = threading.Thread(target=mic_test, daemon=True)
        self._mic_thread.start()
    
    def show(self):
        self.root.deiconify()
    
    def close(self):
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()
