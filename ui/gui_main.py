import tkinter as tk
from tkinter import ttk
import threading
from core.logger import app_logger

class VoiceAssistantGUI:
    """Basic GUI for Voice Assistant"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("600x400")
        self.root.configure(bg='#1e1e1e')
        
        self._setup_ui()
        app_logger.info("GUI initialized")
    
    def _setup_ui(self):
        """Setup UI elements"""
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_frame,
            text="Voice Assistant",
            font=('Arial', 24, 'bold'),
            bg='#1e1e1e',
            fg='#00d4ff'
        )
        title.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready",
            font=('Arial', 12),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        self.status_label.pack(pady=10)
        
        # Recognized text display
        self.text_display = tk.Text(
            main_frame,
            height=10,
            width=70,
            bg='#2d2d2d',
            fg='#00ff00',
            font=('Courier', 10),
            state=tk.DISABLED
        )
        self.text_display.pack(pady=10)
        
        # Partial result label
        self.partial_label = tk.Label(
            main_frame,
            text="Partial: ",
            font=('Arial', 10),
            bg='#1e1e1e',
            fg='#ffaa00'
        )
        self.partial_label.pack(pady=5)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        button_frame.pack(pady=20)
        
        # Start button
        self.start_btn = tk.Button(
            button_frame,
            text="Start",
            command=self._on_start,
            width=10,
            bg='#00aa00',
            fg='#ffffff',
            font=('Arial', 10),
            relief=tk.RAISED,
            bd=2
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self._on_stop,
            width=10,
            bg='#aa0000',
            fg='#ffffff',
            font=('Arial', 10),
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self._on_clear,
            width=10,
            bg='#0066aa',
            fg='#ffffff',
            font=('Arial', 10),
            relief=tk.RAISED,
            bd=2
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
    
    def _on_start(self):
        """Start button handler"""
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Running...", fg='#00ff00')
        self._log_message("[Assistant started]")
    
    def _on_stop(self):
        """Stop button handler"""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Stopped", fg='#ff0000')
        self.assistant.stop()
        self._log_message("[Assistant stopped]")
    
    def _on_clear(self):
        """Clear button handler"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)
        self.partial_label.config(text="Partial: ")
    
    def _log_message(self, message: str):
        """Add message to text display"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, f"{message}\n")
        self.text_display.see(tk.END)
        self.text_display.config(state=tk.DISABLED)
    
    def update_partial_result(self, partial_text: str):
        """Update partial recognition result"""
        self.partial_label.config(text=f"Partial: {partial_text}")
    
    def show(self):
        """Show GUI window"""
        self.root.deiconify()
    
    def close(self):
        """Close GUI window"""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
    
    def run(self):
        """Run GUI event loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.assistant.stop()
            self.root.destroy()
