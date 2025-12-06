import os
import google.generativeai as genai
from typing import Optional

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", None)

def explain_in_target_lang(topic: str, target_lang: str = "German", audience_level="beginner") -> str:
    """
    Given an English topic or phrase, return an explanation in the target language.
    Uses Gemini API if available; otherwise returns a simple template.
    """
    lang_name = {
        "de": "German",
        "es": "Spanish",
        "fr": "French",
        "en": "English",
        "hi": "Hindi"
    }.get(target_lang, target_lang)

    prompt = f"Explain the following topic in simple {lang_name} for a {audience_level}: {topic}\nKeep sentences short and beginner-friendly."
    
    if GEMINI_KEY:
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Gemini API error: {e}"
    else:
        # Simple fallback: template explanation
        try:
            from transformers import pipeline
            gen = pipeline("text2text-generation", model="google/flan-t5-small")
            out = gen(prompt, max_length=200)
            return out[0]["generated_text"]
        except Exception:
            return f"Sorry, LLM not configured. Please set GEMINI_API_KEY to get {lang_name} responses."

def get_chat_response(user_text: str, context: str = "") -> str:
    """
    General chat response in the same language as user_text (assumed).
    """
    if GEMINI_KEY:
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"{context}\nUser: {user_text}\nAssistant:"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Gemini API error: {e}"
    return "I am listening. (Note: To get smart responses, please add your GEMINI_API_KEY to Streamlit Secrets.)"

if __name__ == "__main__":
    print(explain_in_target_lang("How to prepare for IELTS speaking", target_lang="es"))
