import os
import json
import time
from typing import Dict, Any, List
from pathlib import Path
from fastapi import UploadFile
from .exceptions import *
from .config import settings
from .logger import app_logger

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        app_logger.error(f"Failed to load config: {e}")
        return {}

def save_audio_file(audio_data: bytes, filename: str, directory: str = "temp") -> str:
    try:
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        app_logger.info(f"Saved audio file: {filepath}")
        return filepath
    except Exception as e:
        app_logger.error(f"Failed to save audio file: {e}")
        raise AudioProcessingException(f"Could not save audio file: {e}")

def validate_language_code(lang_code: str) -> bool:
    return lang_code in settings.supported_languages

def validate_audio_file(file: UploadFile, max_size_mb: int, supported_formats: List[str]) -> None:
    if not file.filename:
        raise AudioProcessingException("No filename provided")
    
    ext = Path(file.filename).suffix.lower().lstrip('.')
    if ext not in supported_formats:
        raise AudioProcessingException(f"Unsupported format: {ext}. Supported: {supported_formats}")
    
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if size > max_size_bytes:
        raise FileSizeException(f"File too large: {size/1024/1024:.1f}MB. Max: {max_size_mb}MB")

def cleanup_temp_files(directory: str = "temp", max_age_hours: int = 24) -> None:
    try:
        now = time.time()
        for file_path in Path(directory).glob("*"):
            if file_path.is_file():
                age_hours = (now - file_path.stat().st_mtime) / 3600
                if age_hours > max_age_hours:
                    file_path.unlink()
                    app_logger.info(f"Cleaned up old file: {file_path}")
    except Exception as e:
        app_logger.error(f"Cleanup failed: {e}")

def format_response(success: bool, data: Any = None, message: str = "") -> Dict:
    return {
        "success": success,
        "data": data,
        "message": message,
        "timestamp": int(time.time())
    }