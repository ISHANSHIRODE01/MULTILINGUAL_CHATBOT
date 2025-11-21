import os
import google.generativeai as genai
from typing import Optional

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", None)

def explain_in_simple_german(topic: str, audience_level="beginner") -> str:
    """
    Given an English topic or German phrase, return an explanation in simple German.
    Uses Gemini API if available; otherwise returns a simple template.
    """
    prompt = f"Explain the following topic in simple German for a {audience_level}: {topic}\nKeep sentences short and beginner-friendly."
    
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
            return "Entschuldigung — LLM nicht konfiguriert. Bitte setze GEMINI_API_KEY."

if __name__ == "__main__":
    print(explain_in_simple_german("How to prepare for IELTS speaking"))
