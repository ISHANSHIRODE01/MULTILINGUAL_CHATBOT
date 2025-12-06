# src/backend/translator.py
"""
Simple EN<->DE translator using MarianMT from Hugging Face.
For small/fast demos, this works offline.
"""
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
from .exceptions import TranslationException
from .logger import app_logger

MODEL_CACHE = {}

def load_model_pair(src_tgt="en-de"):
    try:
        if src_tgt in MODEL_CACHE:
            return MODEL_CACHE[src_tgt]
        if src_tgt == "en-de":
            model_name = "Helsinki-NLP/opus-mt-en-de"
        elif src_tgt == "de-en":
            model_name = "Helsinki-NLP/opus-mt-de-en"
        else:
            raise TranslationException(f"Unsupported translation pair: {src_tgt}")
        
        tok = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        MODEL_CACHE[src_tgt] = (tok, model)
        app_logger.info(f"Loaded translation model: {model_name}")
        return tok, model
    except Exception as e:
        app_logger.error(f"Failed to load translation model: {e}")
        raise TranslationException(f"Model loading failed: {e}")

def detect_language(text: str) -> dict:
    try:
        lang = detect(text)
        return {"language": lang, "confidence": 0.9}
    except Exception as e:
        app_logger.error(f"Language detection failed: {e}")
        return {"language": "unknown", "confidence": 0.0}

def translate(text: str, src="en", tgt="de") -> dict:
    try:
        pair = f"{src}-{tgt}"
        tok, model = load_model_pair(pair)
        batch = tok([text], return_tensors="pt", padding=True)
        out = model.generate(**batch, max_length=512)
        translated = tok.batch_decode(out, skip_special_tokens=True)[0]
        
        app_logger.info(f"Translation completed: {src} -> {tgt}")
        return {
            "translated_text": translated,
            "source_language": src,
            "target_language": tgt,
            "confidence": 0.9
        }
    except Exception as e:
        app_logger.error(f"Translation failed: {e}")
        raise TranslationException(f"Translation failed: {e}")

if __name__ == "__main__":
    print(translate("How to prepare for IELTS speaking?", "en", "de"))
