import datetime
import os
import subprocess
import webbrowser
from typing import Tuple, Any
from core.logger import app_logger, log_error, log_command
from config.settings import config

class CommandRouter:
    """Routes and executes voice commands"""
    
    def __init__(self):
        self.commands = {
            'time': self._cmd_time,
            'date': self._cmd_date,
            'google': self._cmd_google,
            'youtube': self._cmd_youtube,
            'calculator': self._cmd_calculator,
            'notepad': self._cmd_notepad,
            'weather': self._cmd_weather,
            'shutdown': self._cmd_shutdown,
            'restart': self._cmd_restart,
            'lock': self._cmd_lock,
            'hello': self._cmd_hello,
        }
        app_logger.info("CommandRouter initialized with %d commands", len(self.commands))
    
    def route_command(self, text: str) -> Tuple[str, str, bool]:
        """Route command and return (command_type, result, success)"""
        try:
            text_lower = text.lower().strip()
            
            for cmd_name, cmd_func in self.commands.items():
                if cmd_name in text_lower:
                    log_command(text, cmd_name)
                    result = cmd_func(text_lower)
                    return (cmd_name, result, True)
            
            log_command(text, 'unknown', 'not_recognized')
            return ('unknown', 'Команда не распознана', False)
            
        except Exception as e:
            log_error("CommandRouter.route_command", e)
            return ('error', 'Ошибка при роутинге команды', False)
    
    def _cmd_time(self, text: str) -> str:
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime('%H:%M:%S')
        return f"Сейчас {time_str}"
    
    def _cmd_date(self, text: str) -> str:
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime('%d.%m.%Y')
        return f"сегодня {date_str}"
    
    def _cmd_google(self, text: str) -> str:
        """Open Google"""
        query = text.replace('google', '').strip()
        if query:
            webbrowser.open(f'https://www.google.com/search?q={query}')
            return f"Поиск Google по запросу: {query}"
        else:
            webbrowser.open('https://www.google.com')
            return "Открываю Google"
    
    def _cmd_youtube(self, text: str) -> str:
        """Open YouTube"""
        query = text.replace('youtube', '').replace('ютуб', '').strip()
        if query:
            webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
            return f"Поиск YouTube: {query}"
        else:
            webbrowser.open('https://www.youtube.com')
            return "Открываю YouTube"
    
    def _cmd_calculator(self, text: str) -> str:
        """Open calculator"""
        try:
            subprocess.Popen('calc.exe')
            return "Открываю калькулятор"
        except Exception as e:
            log_error("_cmd_calculator", e)
            return "Не удалось открыть калькулятор"
    
    def _cmd_notepad(self, text: str) -> str:
        """Open notepad"""
        try:
            subprocess.Popen('notepad.exe')
            return "Открываю блокнот"
        except Exception as e:
            log_error("_cmd_notepad", e)
            return "Не удалось открыть блокнот"
    
    def _cmd_weather(self, text: str) -> str:
        """Get weather info (placeholder)"""
        return "Ничего не найдено в настоящие эпохи"
    
    def _cmd_shutdown(self, text: str) -> str:
        """Shutdown system"""
        try:
            subprocess.run(['shutdown', '/s', '/t', '60'], check=True)
            return "Компьютер выключится через 60 секунд"
        except Exception as e:
            log_error("_cmd_shutdown", e)
            return "Ошибка при выключении"
    
    def _cmd_restart(self, text: str) -> str:
        """Restart system"""
        try:
            subprocess.run(['shutdown', '/r', '/t', '60'], check=True)
            return "Компьютер перезагружится через 60 секунд"
        except Exception as e:
            log_error("_cmd_restart", e)
            return "Ошибка при перезагрузке"
    
    def _cmd_lock(self, text: str) -> str:
        """Lock system"""
        try:
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=True)
            return "Компьютер заблокирован"
        except Exception as e:
            log_error("_cmd_lock", e)
            return "Ошибка при блокировке"
    
    def _cmd_hello(self, text: str) -> str:
        """Greeting response"""
        return "Привет! Что вы хотите сделать?"
