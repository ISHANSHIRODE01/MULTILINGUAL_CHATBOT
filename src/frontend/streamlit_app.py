import streamlit as st
import requests
import os
from pathlib import Path
import time
import base64

# Configuration
# Priority: Streamlit Secrets -> Env Var -> Docker Localhost
if "API_BASE" in st.secrets:
    API_BASE = st.secrets["API_BASE"]
else:
    API_BASE = os.getenv("API_BASE", "http://localhost:8080")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_FORMATS = ["wav", "mp3", "m4a", "ogg"]

st.set_page_config(
    page_title="Multilingual Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Glassmorphism Theme
st.markdown("""
    <style>
    /* Global Reset & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(10, 10, 20) 90%);
        color: #e2e8f0;
    }
    
    /* Glassmorphism Containers */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat Bubbles */
    .chat-bubble {
        padding: 15px 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        max-width: 80%;
        line-height: 1.5;
        position: relative;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .bot-bubble {
        background: rgba(51, 65, 85, 0.8);
        color: #f1f5f9;
        margin-right: auto;
        border-bottom-left-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Status Indicators */
    .status-dot {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .status-online { background-color: #22c55e; box-shadow: 0 0 10px rgba(34, 197, 94, 0.5); }
    .status-offline { background-color: #ef4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.5); }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 12px;
        padding: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.1);
        transition: border-color 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #3b82f6;
    }
    </style>
""", unsafe_allow_html=True)

# Helper for chat bubbles
def render_chat_message(role, text, lang=None):
    css_class = "user-bubble" if role == "user" else "bot-bubble"
    icon = "👤" if role == "user" else "🤖"
    lang_badge = f"<span style='font-size: 0.8em; opacity: 0.7; margin-left: 8px; background: rgba(0,0,0,0.2); padding: 2px 6px; border-radius: 4px;'>{lang.upper()}</span>" if lang else ""
    
    st.markdown(f"""
        <div class="chat-bubble {css_class}">
            <div style="font-size: 0.8em; opacity: 0.8; margin-bottom: 4px;">{icon} {role.title()} {lang_badge}</div>
            {text}
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    # API Status
    try:
        health_resp = requests.get(f"{API_BASE}/health", timeout=2)
        if health_resp.status_code == 200:
            st.markdown('<div><span class="status-dot status-online"></span>System Online</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div><span class="status-dot status-offline"></span>System Offline</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div><span class="status-dot status-offline"></span>System Offline</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 🌐 Settings")
    target_lang = st.selectbox(
        "Target Language",
        options=["de", "es", "fr"],
        format_func=lambda x: {"de": "German 🇩🇪", "es": "Spanish 🇪🇸", "fr": "French 🇫🇷"}[x],
        index=0
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("### 💡 Tips")
    st.info("Try saying: 'Hello, how are you?' to see how it translates and responds in German!")
    st.markdown('</div>', unsafe_allow_html=True)

# Chat Input (Text)
if prompt := st.chat_input("Type a message..."):
    # Add User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "lang": "auto"
    })
    
    # Process
    try:
        payload = {"text": prompt, "target_lang": target_lang}
        resp = requests.post(f"{API_BASE}/chat_text", json=payload, timeout=45)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                res = data.get("data", {})
                
                # Add Bot Message
                bot_msg = {
                    "role": "assistant",
                    "content": res.get("reply_text"),
                    "lang": target_lang,
                    "grammar": res.get("grammar_matches", [])
                }
                
                # Handle Audio
                audio_path = res.get("reply_audio_path")
                if audio_path and Path(audio_path).exists():
                    with open(audio_path, "rb") as f:
                        bot_msg["audio"] = f.read()
                
                st.session_state.messages.append(bot_msg)
                st.rerun()
            else:
                st.error(f"Error: {data.get('message')}")
        else:
            st.error("Server Error")
    except Exception as e:
        st.error(f"Connection Failed: {e}")
