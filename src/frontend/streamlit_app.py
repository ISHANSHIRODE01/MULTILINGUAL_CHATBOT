import streamlit as st
import os
import asyncio
from pathlib import Path
import uuid
import time
import base64

# Import backend modules directly
from src.agents.orchestrator import handle_audio_interaction, handle_text_interaction

# Page Config
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

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    # System Status (Internal)
    st.markdown('<div><span class="status-dot status-online"></span>System Ready</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 🌐 Settings")
    target_lang = st.selectbox(
        "Target Language",
        options=["de", "es", "fr", "hi"],
        format_func=lambda x: {"de": "German 🇩🇪", "es": "Spanish 🇪🇸", "fr": "French 🇫🇷", "hi": "Hindi 🇮🇳"}.get(x, x),
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()
    with col_b:
        # Export Chat
        chat_text = "Conversation History\n\n"
        for msg in st.session_state.messages:
            role = msg["role"].upper()
            content = msg["content"]
            chat_text += f"[{role}]: {content}\n\n"
            
        st.download_button(
            label="💾 Save",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("# 🤖 Multilingual Assistant")
    st.markdown("*Experience seamless voice conversations.*")
    
    # Chat Container
    st.markdown('<div class="glass-container" style="min-height: 400px;">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.info("👋 Welcome! Speak or type to start the conversation.")
    
    for msg in st.session_state.messages:
        render_chat_message(msg["role"], msg["content"], msg.get("lang"))
        if "audio" in msg and msg["audio"]:
            st.audio(msg["audio"])
        if "grammar" in msg and msg["grammar"]:
            with st.expander("📝 Grammar Corrections"):
                for m in msg["grammar"]:
                    st.warning(f"• {m['message']}")
                    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input Area
    st.markdown("### 🎙️ Voice Input")
    
    # Microphone Input
    audio_buffer = st.audio_input("Record Audio")
    
    # File Uploader
    uploaded = st.file_uploader("Or Upload Audio File", type=["wav", "mp3", "m4a", "ogg"])
    
    # Determine which input to use
    input_audio = audio_buffer if audio_buffer else uploaded
    
    if input_audio:
        # Check if this file was already processed to avoid re-processing on rerun
        # Use a unique key based on file name or size/content if possible
        file_key = f"{input_audio.name}_{input_audio.size}"
        
        if "last_processed" not in st.session_state or st.session_state.last_processed != file_key:
            if st.button("🚀 Process Audio", type="primary"):
                with st.spinner("🔄 Transcribing & Translating..."):
                    try:
                        # Save temp file
                        temp_dir = Path("temp")
                        temp_dir.mkdir(exist_ok=True)
                        temp_path = temp_dir / f"{uuid.uuid4().hex}.wav"
                        
                        with open(temp_path, "wb") as f:
                            f.write(input_audio.getbuffer())
                        
                        # Process directly using orchestrator
                        result = asyncio.run(handle_audio_interaction(str(temp_path), target_lang=target_lang))
                        
                        # Cleanup
                        if temp_path.exists():
                            temp_path.unlink()

                        # Add User Message
                        st.session_state.messages.append({
                            "role": "user",
                            "content": result["user_text"],
                            "lang": result["detected_lang"]
                        })
                        
                        # Add Bot Message
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result["reply_text"],
                            "lang": target_lang,
                            "audio": result["reply_audio_path"],
                            "grammar": result["grammar_matches"]
                        })
                        
                        st.session_state.last_processed = file_key
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

with col2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("### 🎯 Features")
    st.markdown("""
    - **Whisper ASR**: High-fidelity speech recognition
    - **Gemini LLM**: Context-aware translations
    - **Neural TTS**: Natural voice synthesis
    - **Grammar Coach**: Real-time feedback
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("### 💡 Tips")
    st.info("Try saying: 'Hello, how are you?' to see how it translates and responds!")
    st.markdown('</div>', unsafe_allow_html=True)

# Chat Input (Text)
if prompt := st.chat_input("Type a message..."):
    # Add User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "lang": "auto"
    })
    
    with st.spinner("Thinking..."):
        try:
            # Process directly using orchestrator
            result = asyncio.run(handle_text_interaction(prompt, target_lang=target_lang))
            
            # Add Bot Message
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["reply_text"],
                "lang": target_lang,
                "audio": result["reply_audio_path"],
                "grammar": result["grammar_matches"]
            })
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
    st.rerun()
