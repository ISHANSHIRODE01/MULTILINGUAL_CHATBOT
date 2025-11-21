# src/agents/orchestrator.py
"""
Simple orchestrator that ties ASR -> translate -> LLM -> TTS -> feedback
Returns structured dict suitable for frontends.
"""
import os
from pathlib import Path
from ..backend import asr, tts, translator, llm_helper, feedback

MEMORY_FILE = Path("memory.json")

import json

def handle_audio_interaction(audio_path: str, user_lang_hint: str = None, target_lang: str = "de"):
    """
    Steps:
    1) transcribe
    2) detect language (we rely on ASR result)
    3) if transcribed language != target_lang and user asked in EN, translate to DE
    4) ask LLM to explain in simple German
    5) grammar feedback on LLM text (optional)
    6) synthesize TTS
    7) compute pronunciation score if user wants to repeat a phrase (optional)
    """
    tr = asr.transcribe(audio_path, lang_hint=user_lang_hint)
    user_text = tr["text"]
    detected = tr.get("lang", None)
    # If user spoke English but we want German reply, we generate in German.
    prompt_topic = user_text
    reply_text = llm_helper.explain_in_simple_german(prompt_topic)
    # grammar correct the reply (de)
    grammar = feedback.grammar_correct(reply_text, lang="de")
    # synthesize
    out_audio = tts.synthesize_to_file(grammar["corrected"], None, lang="de")
    # store memory (append)
    memory = []
    if MEMORY_FILE.exists():
        try:
            memory = json.loads(MEMORY_FILE.read_text())
        except Exception:
            memory = []
    memory.append({"user": user_text, "reply": grammar["corrected"]})
    MEMORY_FILE.write_text(json.dumps(memory[-20:], ensure_ascii=False, indent=2))
    return {
        "user_text": user_text,
        "detected_lang": detected,
        "reply_text": grammar["corrected"],
        "reply_audio_path": out_audio,
        "grammar_matches": grammar["matches"]
    }

if __name__ == "__main__":
    # basic local test (point to a file)
    import sys
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py sample.wav")
    else:
        print(handle_audio_interaction(sys.argv[1]))
