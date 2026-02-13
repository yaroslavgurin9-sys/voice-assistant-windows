@echo off
REM Voice Assistant Quick Launcher for Windows

REM Navigate to project directory
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the assistant
python main.py

pause
