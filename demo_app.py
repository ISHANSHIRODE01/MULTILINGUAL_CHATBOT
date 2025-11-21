import streamlit as st

st.set_page_config(page_title="Multilingual Chatbot Demo", page_icon="🗣️")

st.title("🗣️ Multilingual Voice Chatbot")
st.markdown("**Demo Version** - Upload audio to see the interface")

st.info("💡 This is a demo of the chatbot interface. The full version includes:")
st.markdown("""
- 🎤 **Speech Recognition** (ASR)
- 🌍 **Language Translation** 
- 🤖 **AI Language Learning**
- 🔊 **Text-to-Speech**
- 📝 **Grammar Feedback**
""")

uploaded = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])

if uploaded:
    st.success(f"File uploaded: {uploaded.name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Input")
        st.audio(uploaded)
        
    with col2:
        st.header("Results")
        st.info("🌍 Detected: **English**")
        st.markdown("### 🇩🇪 German Translation")
        st.write("Hallo! Wie geht es dir heute?")
        st.success("✅ No grammar issues detected")

st.markdown("---")
st.markdown("Built with Streamlit & FastAPI | [View Code](https://github.com/yourusername/multilingual-chatbot)")