# src/backend/feedback.py
"""
Grammar correction and pronunciation scoring.
Grammar: language_tool_python (wraps LanguageTool)
Pronunciation scoring: simple proxy comparing reference_text vs ASR transcription
"""
from typing import Tuple, Dict
import language_tool_python
import difflib
from .asr import transcribe

_tool_cache = {}

def _get_tool(lang_code="en"):
    # language_tool_python supports codes like 'en-US', 'de-DE'
    key = lang_code
    if key not in _tool_cache:
        try:
            _tool_cache[key] = language_tool_python.LanguageTool('de') if 'de' in lang_code else language_tool_python.LanguageTool('en-US')
        except Exception:
            _tool_cache[key] = None
    return _tool_cache[key]

def grammar_correct(text: str, lang="de") -> Dict:
    tool = _get_tool(lang)
    if not tool:
        return {"corrected": text, "matches": []}
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    # simplify matches
    simple = [{"offset": m.offset, "length": m.errorLength, "message": m.message, "replacements": m.replacements} for m in matches]
    return {"corrected": corrected, "matches": simple}

def pronunciation_score(audio_path: str, reference_text: str) -> Dict:
    """
    Proxy pronunciation score:
    - transcribe audio and compare words to reference_text
    - compute word-level similarity ratio
    """
    asr_res = transcribe(audio_path, lang_hint="de")
    asr_text = asr_res.get("text", "")
    # token-level compare
    ref_words = reference_text.lower().split()
    hyp_words = asr_text.lower().split()
    seq = difflib.SequenceMatcher(a=ref_words, b=hyp_words)
    score = int(seq.ratio() * 100)
    return {"ref": reference_text, "asr": asr_text, "score": score, "ratio": seq.ratio()}

if __name__ == "__main__":
    print(grammar_correct("Ich gehe in die Universität. Ich lerne gut.", "de"))
