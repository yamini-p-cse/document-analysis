from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
import uuid
import tempfile
from models.response_models import SentimentEnum
from utils.document_processor import DocumentProcessor
from utils.ai_analyzer import AIAnalyzer

app = FastAPI(title="AI Document Analysis API v2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

analyzer = AIAnalyzer()
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
        
        text = DocumentProcessor.extract_text(file_path)
        if not text:
            return {"status": "error", "message": "No text extracted"}
        
        analysis = analyzer.analyze(text)
        
        return {
            "status": "success",
            "fileName": request.fileName,
            "summary": analysis["summary"],
            "entities": {
                "names": analysis["entities"].get("PERSON", []),
                "dates": analysis["entities"].get("DATE", []),
                "organizations": analysis["entities"].get("ORG", []),
                "amounts": analysis["entities"].get("MONEY", [])
            },
            "sentiment": analysis["sentiment"].capitalize()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.unlink(file_path)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <h1>🚀 AI Document Analysis API</h1>
    <p><b>Endpoint:</b> POST /api/document-analyze</p>
    <p><b>API Key:</b> sk_track2_987654321</p>
    <p><a href="/docs">API Docs</a> | <a href="https://github.com/">GitHub</a></p>
    """
    return HTMLResponse(content=html)