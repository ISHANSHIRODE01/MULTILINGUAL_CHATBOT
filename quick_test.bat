@echo off
echo Testing Multilingual Chatbot System...
echo.

echo 1. Running system tests...
python test_system.py

echo.
echo 2. Starting backend (will open in new window)...
start "Backend" cmd /k "python -m uvicorn src.backend.app:app --port 8000"

timeout /t 3 /nobreak > nul

echo 3. Starting frontend...
streamlit run src\frontend\streamlit_app.py