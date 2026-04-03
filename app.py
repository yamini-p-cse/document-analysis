from fastapi import FastAPI, HTTPException, Header, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
import uuid
import tempfile
from models.response_models import SentimentEnum  # Keep if exists
from utils.document_processor import DocumentProcessor  # Keep if exists

app = FastAPI(title="AI Document Analysis API v2.0")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Comment out AI analyzer (not installed on Vercel)
# from utils.ai_analyzer import AIAnalyzer
# analyzer = AIAnalyzer()

API_KEY = "sk_track2_987654321"

class DocumentRequest(BaseModel):
    fileName: str
    fileType: str
    fileBase64: str

@app.post("/api/document-analyze")
async def analyze_document(request: DocumentRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        file_bytes = base64.b64decode(request.fileBase64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{request.fileType}") as tmp:
            tmp.write(file_bytes)
            file_path = tmp.name
        
        # Extract text (works without AI)
        text = DocumentProcessor.extract_text(file_path)
        if not text:
            return {"status": "error", "message": "No text extracted"}
        
        # Basic analysis (no AI needed)
        char_count = len(text)
        word_count = len(text.split())
        
        # Mock AI response (add real AI later)
        analysis = {
            "summary": text[:500] + "..." if len(text) > 500 else text,
            "entities": {"PERSON": [], "DATE": [], "ORG": [], "MONEY": []},
            "sentiment": "neutral"
        }
        
        return {
            "status": "success",
            "fileName": request.fileName,
            "text_preview": text[:200] + "...",
            "char_count": char_count,
            "word_count": word_count,
            "summary": analysis["summary"],
            "entities": analysis["entities"],
            "sentiment": analysis["sentiment"].capitalize(),
            "note": "Full AI analysis coming soon via external API!"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.unlink(file_path)

# NEW: Simple file upload endpoint (easier testing)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_extension = file.filename.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
        tmp.write(contents)
        file_path = tmp.name
    
    text = DocumentProcessor.extract_text(file_path)
    
    return {
        "filename": file.filename,
        "text_preview": text[:200] + "..." if text else "No text extracted",
        "word_count": len(text.split()) if text else 0
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <h1>🚀 Document Analysis API - LIVE!</h1>
    <p><b>✅ Basic PDF/DOCX parsing working</b></p>
    <ul>
        <li><b>POST /api/document-analyze</b> (API Key: sk_track2_987654321)</li>
        <li><b>POST /upload</b> (file upload test)</li>
        <li><a href="/docs">📖 FastAPI Docs</a></li>
    </ul>
    <p><i>Full AI features coming soon!</i></p>
    """
    return HTMLResponse(content=html)