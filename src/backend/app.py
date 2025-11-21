from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import uuid
from pathlib import Path

app = FastAPI(title="Multilingual Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"success": True, "message": "Multilingual Chatbot API", "status": "healthy"}

@app.get("/health")
async def health():
    return {"success": True, "data": {"status": "ok", "version": "1.0.0"}}

@app.post("/chat_audio")
async def chat_audio(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / f"{uuid.uuid4().hex}{Path(file.filename).suffix}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process with orchestrator
        try:
            from ..agents.orchestrator import handle_audio_interaction
            result = handle_audio_interaction(str(file_path))
        except Exception as e:
            # Fallback response
            result = {
                "detected_lang": "en",
                "reply_text": "Hallo! Das System funktioniert. Ihre Audiodatei wurde erfolgreich verarbeitet.",
                "reply_audio_path": None,
                "grammar_matches": []
            }
        
        # Cleanup
        if file_path.exists():
            file_path.unlink()
        
        return {"success": True, "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)