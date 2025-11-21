# src/backend/tts.py
"""
Simple offline TTS wrapper using pyttsx3.
Note: pyttsx3 voices vary by OS. For better TTS (German), consider Coqui TTS / gTTS / cloud TTS.
"""

import pyttsx3
import tempfile
import os
from typing import Optional
from .exceptions import TTSException
from .logger import app_logger

_engine = None

def _init_engine():
    global _engine
    try:
        if _engine is None:
            _engine = pyttsx3.init()
            voices = _engine.getProperty('voices')
            for v in voices:
                lname = v.name.lower() + " " + (v.id.lower() if v.id else "")
                if "german" in lname or "de" in lname:
                    _engine.setProperty('voice', v.id)
                    app_logger.info(f"Set German voice: {v.name}")
                    break
        return _engine
    except Exception as e:
        app_logger.error(f"TTS engine initialization failed: {e}")
        raise TTSException(f"TTS initialization failed: {e}")

def synthesize(text: str, language: str = "de", output_path: Optional[str] = None) -> str:
    try:
        engine = _init_engine()
        if output_path is None:
            fd, path = tempfile.mkstemp(suffix=".mp3", dir="temp")
            os.close(fd)
        else:
            path = output_path
            os.makedirs(os.path.dirname(path), exist_ok=True)
        
        engine.save_to_file(text, path)
        engine.runAndWait()
        app_logger.info(f"TTS synthesis completed: {path}")
        return path
    except Exception as e:
        app_logger.error(f"TTS synthesis failed: {e}")
        raise TTSException(f"TTS synthesis failed: {e}")

def synthesize_to_file(text: str, out_path: Optional[str] = None, lang: str = "en") -> str:
    return synthesize(text, lang, out_path)

if __name__ == "__main__":
    p = synthesize_to_file("Hallo, das ist ein Test.", None, lang="de")
    print("Wrote:", p)
