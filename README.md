# Multilingual Chatbot

A multilingual voice chatbot that processes audio input and provides German responses with grammar feedback.

## Features

- **ASR (Speech Recognition)**: OpenAI Whisper for transcription
- **Translation**: MarianMT (Helsinki-NLP) for EN↔DE translation
- **LLM Integration**: Gemini API for German explanations
- **TTS (Text-to-Speech)**: pyttsx3 for audio generation
- **Grammar Checking**: LanguageTool for corrections
- **Web Interface**: Streamlit frontend

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Key** (optional):
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_key_here" > .env
   ```

3. **Start Backend**:
   ```bash
   python src/backend/app.py
   ```

4. **Start Frontend** (new terminal):
   ```bash
   streamlit run src/frontend/streamlit_app.py
   ```

5. **Open Browser**: http://localhost:8501

## Usage

1. Upload an audio file (wav, mp3, m4a)
2. Click "Process Audio"
3. Get German translation with grammar feedback
4. Listen to TTS audio response

## Technology Stack

| Component | Technology | Status |
|-----------|------------|--------|
| ASR | OpenAI Whisper | ✅ Free/Offline |
| Translation | MarianMT | ✅ Free/Offline |
| LLM | Gemini API | ✅ Free Tier |
| TTS | pyttsx3 | ✅ Free/Offline |
| Grammar | LanguageTool | ✅ Free |
| Backend | FastAPI | ✅ |
| Frontend | Streamlit | ✅ |

## Project Structure

```
multilingual-chatbot/
├── src/
│   ├── backend/
│   │   ├── app.py              # FastAPI server
│   │   ├── asr.py              # Speech recognition
│   │   ├── tts.py              # Text-to-speech
│   │   ├── translator.py       # Translation
│   │   ├── feedback.py         # Grammar checking
│   │   └── llm_helper.py       # LLM integration
│   ├── frontend/
│   │   └── streamlit_app.py    # Web interface
│   └── agents/
│       └── orchestrator.py     # Workflow coordination
├── requirements.txt            # Dependencies
├── .env                       # API keys
└── README.md                  # This file
```