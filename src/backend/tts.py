import edge_tts
import asyncio
from .logger import app_logger
from .exceptions import TTSException
from typing import Optional

# Voice mapping
VOICES = {
    "en": "en-US-AriaNeural",
    "de": "de-DE-KatjaNeural",
    "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-DeniseNeural"
}

async def synthesize(text: str, lang: str = "en", output_file: Optional[str] = None) -> str:
    """
    Synthesize text to speech using edge-tts (async).
    """
    try:
        voice = VOICES.get(lang, "en-US-AriaNeural")
        communicate = edge_tts.Communicate(text, voice)
        
        if output_file:
            await communicate.save(output_file)
            app_logger.info(f"TTS synthesis completed: {output_file}")
            return output_file
        else:
            # If no file path provided, we can't easily return audio bytes without a temp file in this lib
            # But for our use case we always provide a path.
            raise TTSException("Output file path is required for edge-tts")
            
    except Exception as e:
        app_logger.error(f"TTS failed: {e}")
        raise TTSException(f"TTS failed: {e}")

async def synthesize_to_file(text: str, out_path: str, lang: str = "en") -> str:
    return await synthesize(text, lang, out_path)
