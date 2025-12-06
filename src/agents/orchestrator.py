# src/agents/orchestrator.py
"""
Simple orchestrator that ties ASR -> translate -> LLM -> TTS -> feedback
Returns structured dict suitable for frontends.
"""
import os
from pathlib import Path
from ..backend import asr, tts, translator, llm_helper, feedback
import uuid
from ..backend.logger import app_logger
from langdetect import detect

MEMORY_FILE = Path("memory.json")

import json

async def _process_text(user_text: str, detected_lang: str, target_lang: str) -> dict:
    """
    Core logic for processing text:
    - Grammar check (if target lang)
    - LLM response
    - TTS generation
    """
    reply_text = ""
    grammar_matches = []
    
    try:
        if detected_lang == target_lang:
            # Check grammar
            grammar_matches = feedback.grammar_correct(user_text, lang=target_lang)
            # Reply
            reply_text = llm_helper.get_chat_response(user_text, context=f"User is practicing {target_lang}.")
        else:
            # Translate/Explain
            reply_text = llm_helper.explain_in_target_lang(user_text, target_lang=target_lang)
            
        app_logger.info(f"Bot reply: {reply_text}")
        
        # TTS
        out_filename = f"response_{uuid.uuid4().hex}.mp3"
        out_path = os.path.join("temp", out_filename)
        os.makedirs("temp", exist_ok=True)
        
        # Async TTS call
        await tts.synthesize_to_file(reply_text, out_path, lang=target_lang)
        
        # store memory (append)
        memory = []
        if MEMORY_FILE.exists():
            try:
                memory = json.loads(MEMORY_FILE.read_text())
            except Exception:
                memory = []
        memory.append({"user": user_text, "reply": reply_text, "lang": target_lang})
        MEMORY_FILE.write_text(json.dumps(memory[-20:], ensure_ascii=False, indent=2))

        return {
            "user_text": user_text,
            "detected_lang": detected_lang,
            "reply_text": reply_text,
            "reply_audio_path": out_path,
            "grammar_matches": grammar_matches
        }
    except Exception as e:
        app_logger.error(f"Processing error: {e}")
        raise e

async def handle_audio_interaction(audio_path: str, user_lang_hint: str = None, target_lang: str = "de"):
    try:
        tr = asr.transcribe(audio_path, lang_hint=user_lang_hint)
        user_text = tr["text"]
        detected = tr.get("lang", None)
        
        app_logger.info(f"Audio User said ({detected}): {user_text}")
        
        return await _process_text(user_text, detected, target_lang)
        
    except Exception as e:
        app_logger.error(f"Orchestrator audio error: {e}")
        return {
            "user_text": "(Error)",
            "detected_lang": "unknown",
            "reply_text": f"Error: {e}",
            "reply_audio_path": None,
            "grammar_matches": []
        }

async def handle_text_interaction(user_text: str, target_lang: str = "de"):
    try:
        # Detect language
        try:
            detected = detect(user_text)
        except:
            detected = "en" # fallback
            
        app_logger.info(f"Text User said ({detected}): {user_text}")
        
        return await _process_text(user_text, detected, target_lang)

    except Exception as e:
        app_logger.error(f"Orchestrator text error: {e}")
        return {
            "user_text": user_text,
            "detected_lang": "unknown",
            "reply_text": f"Error: {e}",
            "reply_audio_path": None,
            "grammar_matches": []
        }

if __name__ == "__main__":
    # basic local test
    import sys
    import asyncio
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py sample.wav")
    else:
        print(asyncio.run(handle_audio_interaction(sys.argv[1])))
