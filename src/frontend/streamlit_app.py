import streamlit as st
import requests
import os
from pathlib import Path
import time

# Configuration
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_FORMATS = ["wav", "mp3", "m4a", "ogg"]

st.set_page_config(
    page_title="Multilingual Chatbot",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Multilingual Voice Chatbot")
st.markdown("Upload audio to get German translation with grammar feedback")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    api_status = st.empty()
    
    # Check API health
    try:
        health_resp = requests.get(f"{API_BASE}/health", timeout=5)
        if health_resp.status_code == 200:
            api_status.success("✅ API Connected")
        else:
            api_status.error("❌ API Error")
    except:
        api_status.error("❌ API Unavailable")
    
    st.markdown("---")
    st.markdown("**Supported formats:**")
    st.write(", ".join(SUPPORTED_FORMATS))
    st.markdown(f"**Max file size:** {MAX_FILE_SIZE // (1024*1024)}MB")

# Main interface
tab1, tab2 = st.tabs(["🎤 Audio Translation", "📝 Text Translation"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Upload Audio")
        uploaded = st.file_uploader(
            "Choose an audio file",
            type=SUPPORTED_FORMATS,
            help=f"Maximum file size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    if uploaded:
        # Validate file size
        if uploaded.size > MAX_FILE_SIZE:
            st.error(f"File too large: {uploaded.size / (1024*1024):.1f}MB. Max: {MAX_FILE_SIZE // (1024*1024)}MB")
        else:
            st.success(f"File loaded: {uploaded.name} ({uploaded.size / 1024:.1f}KB)")
            
            if st.button("🎯 Process Audio", type="primary"):
                with st.spinner("Processing audio..."):
                    try:
                        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                        resp = requests.post(f"{API_BASE}/chat_audio", files=files, timeout=30)
                        
                        if resp.status_code == 200:
                            data = resp.json()
                            if data.get("success"):
                                result_data = data.get("data", {})
                                
                                with col2:
                                    st.header("Results")
                                    
                                    # Language detection
                                    detected_lang = result_data.get("detected_lang", "unknown")
                                    st.info(f"🌍 Detected language: **{detected_lang.upper()}**")
                                    
                                    # German translation
                                    reply_text = result_data.get("reply_text", "")
                                    if reply_text:
                                        st.markdown("### 🇩🇪 German Translation")
                                        st.write(reply_text)
                                    
                                    # Grammar feedback
                                    grammar_matches = result_data.get("grammar_matches", [])
                                    if grammar_matches:
                                        st.markdown("### 📝 Grammar Suggestions")
                                        for match in grammar_matches:
                                            st.write(f"• {match}")
                                    else:
                                        st.success("✅ No grammar issues detected")
                                    
                                    # Audio playback
                                    audio_path = result_data.get("reply_audio_path")
                                    if audio_path and Path(audio_path).exists():
                                        st.markdown("### 🔊 Audio Reply")
                                        try:
                                            with open(audio_path, "rb") as audio_file:
                                                audio_bytes = audio_file.read()
                                            st.audio(audio_bytes, format="audio/mp3")
                                        except Exception as e:
                                            st.error(f"Could not load audio: {e}")
                                    else:
                                        st.warning("⚠️ Audio reply not available")
                            else:
                                st.error(f"API Error: {data.get('message', 'Unknown error')}")
                        else:
                            st.error(f"Request failed: {resp.status_code} - {resp.text}")
                            
                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request timed out. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("🔌 Could not connect to API. Check if backend is running.")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {e}")

with tab2:
    st.header("📝 Text Translation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        
        # Language selection
        source_lang = st.selectbox(
            "Source Language",
            options=["auto", "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"],
            format_func=lambda x: "Auto-detect" if x == "auto" else x.upper()
        )
        
        target_lang = st.selectbox(
            "Target Language", 
            options=["de", "en", "es", "fr", "it", "pt", "ru", "zh", "ja", "ko"],
            format_func=lambda x: x.upper()
        )
        
        # Text input
        input_text = st.text_area(
            "Enter text to translate",
            height=150,
            placeholder="Type your text here..."
        )
        
        if st.button("🌍 Translate Text", type="primary"):
            if input_text.strip():
                with st.spinner("Translating..."):
                    try:
                        data = {
                            "text": input_text,
                            "source_lang": source_lang,
                            "target_lang": target_lang
                        }
                        
                        resp = requests.post(f"{API_BASE}/translate_text", data=data, timeout=15)
                        
                        if resp.status_code == 200:
                            result = resp.json()
                            if result.get("success"):
                                result_data = result.get("data", {})
                                
                                with col2:
                                    st.subheader("Translation Result")
                                    
                                    # Show detected language
                                    detected = result_data.get("detected_lang", "unknown")
                                    st.info(f"🌍 Detected: **{detected.upper()}**")
                                    
                                    # Show translation
                                    translated = result_data.get("translated_text", "")
                                    st.markdown(f"### 🇩🇪 Translation ({target_lang.upper()})")
                                    st.write(translated)
                                    
                                    # Grammar feedback
                                    grammar_matches = result_data.get("grammar_matches", [])
                                    if grammar_matches:
                                        st.markdown("### 📝 Grammar Suggestions")
                                        for match in grammar_matches:
                                            st.write(f"• {match}")
                                    else:
                                        st.success("✅ No grammar issues detected")
                                    
                                    # Audio playback
                                    audio_path = result_data.get("audio_path")
                                    if audio_path and Path(audio_path).exists():
                                        st.markdown("### 🔊 Audio")
                                        try:
                                            with open(audio_path, "rb") as f:
                                                audio_bytes = f.read()
                                            st.audio(audio_bytes, format="audio/mp3")
                                        except Exception as e:
                                            st.error(f"Could not load audio: {e}")
                            else:
                                st.error(f"Translation failed: {result.get('message', 'Unknown error')}")
                        else:
                            st.error(f"Request failed: {resp.status_code}")
                            
                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request timed out. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("🔌 Could not connect to API. Check if backend is running.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please enter some text to translate")
    
    with col2:
        st.subheader("Translation Result")
        st.info("👆 Enter text and click translate to see results here")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Multilingual Chatbot v1.0 | "
    "Built with Streamlit & FastAPI</div>",
    unsafe_allow_html=True
)
