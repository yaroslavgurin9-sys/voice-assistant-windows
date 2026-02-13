import logging
import logging.handlers
from pathlib import Path
from config.settings import config

Path(config.logging.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

def setup_logger(name: str, log_file: str, level: str = "INFO"):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=config.logging.MAX_LOG_SIZE, backupCount=config.logging.BACKUP_COUNT, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

app_logger = setup_logger('voice_assistant', config.logging.LOG_FILE, config.logging.LOG_LEVEL)
error_logger = setup_logger('voice_assistant_errors', config.logging.ERROR_LOG_FILE, 'ERROR')

def log_command(recognized_text: str, command_type: str, result: str = "success"):
    app_logger.info(f"COMMAND | Text: '{recognized_text}' | Type: {command_type} | Result: {result}")

def log_error(module: str, error: Exception):
    error_logger.error(f"{module}: {error}", exc_info=True)
    app_logger.error(f"{module}: {error}")
