from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware  # ← ADD THIS
from pydantic import BaseModel
from typing import Optional
import os

from optimizer import optimize_code, analyze_code, chat_with_ai
from pdf_export import generate_pdf_report

app = FastAPI(title="AI Code Optimizer", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request Models ────────────────────────────────────────
class OptimizeRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "all"
    api_key: str

class AnalyzeRequest(BaseModel):
    code: str
    language: str = "python"
    api_key: str

class ChatRequest(BaseModel):
    message: str
    code_context: Optional[str] = ""
    api_key: str

class PDFRequest(BaseModel):
    optimized_code: str
    language: str
    metrics: dict
    analysis: dict

# ── Routes ────────────────────────────────────────────────
@app.post("/api/optimize")
async def optimize(req: OptimizeRequest):
    try:
        result = optimize_code(req.code, req.language, req.mode, req.api_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        result = analyze_code(req.code, req.language, req.api_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        reply = chat_with_ai(req.message, req.code_context, req.api_key)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export-pdf")
async def export_pdf(req: PDFRequest):
    try:
        pdf_bytes = generate_pdf_report(req.dict())
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=optimization-report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)