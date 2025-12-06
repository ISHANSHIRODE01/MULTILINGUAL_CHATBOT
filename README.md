# 🤖 Multilingual AI Chatbot

A powerful, voice-enabled chatbot that helps you practice languages (German 🇩🇪, Spanish 🇪🇸, French 🇫🇷). It uses **Whisper** for speech recognition, **Gemini** for intelligence, and **Edge-TTS** for natural-sounding speech.

![UI Screenshot](https://via.placeholder.com/800x400?text=Multilingual+Chatbot+UI)

## ✨ Features

- **🎙️ Voice & Text Input**: Speak or type your messages.
- **🗣️ Natural Voices**: High-quality AI voices for German, Spanish, and French.
- **🧠 Smart Corrections**: Real-time grammar feedback and explanations.
- **🌍 Multi-Language**: Switch languages instantly.
- **💾 Export History**: Download your conversation transcripts.
- **🐳 Docker Ready**: Easy deployment with Docker Compose.

## 🚀 Quick Start

### Option A: Docker (Recommended)
```bash
docker-compose up --build
```
Access the app at `http://localhost:8501`.

### Option B: Local Python
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set API Key**:
    Create a `.env` file:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```
3.  **Run Backend**:
    ```bash
    python -m src.backend.app
    ```
4.  **Run Frontend** (in a new terminal):
    ```bash
    streamlit run src/frontend/streamlit_app.py
    ```

## 🛠️ Project Structure

```
├── src/
│   ├── backend/          # FastAPI server & logic
│   │   ├── app.py        # API Endpoints
│   │   ├── tts.py        # Edge-TTS integration
│   │   └── ...
│   ├── frontend/         # Streamlit UI
│   │   └── streamlit_app.py
│   └── agents/           # Orchestration logic
├── uploads/              # Temporary audio uploads (auto-cleaned)
├── temp/                 # Temporary TTS files (auto-cleaned)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🧪 Testing

Run the system health check:
```bash
python test_system.py
```

## 📝 License

MIT License