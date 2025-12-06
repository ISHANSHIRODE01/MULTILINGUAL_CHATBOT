from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.on_event("startup")
async def startup_event():
    from .utils import cleanup_temp_files
    # Clean up files older than 24 hours
    cleanup_temp_files("temp", max_age_hours=24)
    cleanup_temp_files("uploads", max_age_hours=24)

@app.get("/health")
async def health():
    return {"success": True, "data": {"status": "ok", "version": "1.0.0"}}

@app.post("/chat_audio")
async def chat_audio(file: UploadFile = File(...), target_lang: str = Form("de")):
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
            result = await handle_audio_interaction(str(file_path), target_lang=target_lang)
        except Exception as e:
            # Fallback response
            result = {
                "user_text": "",
                "detected_lang": "",
                "reply_text": f"Error: {str(e)}",
                "reply_audio_path": None,
                "grammar_matches": []
            }
        
        # Cleanup
        if file_path.exists():
            file_path.unlink()
        
        return {"success": True, "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

class TextRequest(BaseModel):
    text: str
    target_lang: str = "de"

@app.post("/chat_text")
async def chat_text(request: TextRequest):
    try:
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.on_event("startup")
async def startup_event():
    from .utils import cleanup_temp_files
    # Clean up files older than 24 hours
    cleanup_temp_files("temp", max_age_hours=24)
    cleanup_temp_files("uploads", max_age_hours=24)

@app.get("/health")
async def health():
    return {"success": True, "data": {"status": "ok", "version": "1.0.0"}}

@app.post("/chat_audio")
async def chat_audio(file: UploadFile = File(...), target_lang: str = Form("de")):
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
            result = await handle_audio_interaction(str(file_path), target_lang=target_lang)
        except Exception as e:
            # Fallback response
            result = {
                "user_text": "",
                "detected_lang": "",
                "reply_text": f"Error: {str(e)}",
                "reply_audio_path": None,
                "grammar_matches": []
            }
        
        # Cleanup
        if file_path.exists():
            file_path.unlink()
        
        return {"success": True, "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

class TextRequest(BaseModel):
    text: str
    target_lang: str = "de"

@app.post("/chat_text")
async def chat_text(request: TextRequest):
    try:
        from ..agents.orchestrator import handle_text_interaction
        result = await handle_text_interaction(request.text, target_lang=request.target_lang)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="0.0.0.0", port=args.port)