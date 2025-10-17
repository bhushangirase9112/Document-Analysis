import asyncio
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
import time
from models import AnalysisRequest
from utils import extract_text_from_pdf
from agents import summarizer_agent, entity_extractor_agent, sentiment_analyzer_agent

# Configure logging
import logging
logger = logging.getLogger(__name__)

# In-memory storage for job tracking
jobs_store = {}

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt")):
        logger.warning(f"Upload failed: unsupported file type {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    try:
        content = await file.read()
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        else:
            text = content.decode('utf-8')
        if not text or len(text.strip()) < 10:
            logger.warning(f"Upload failed: file {file.filename} is empty or too short.")
            raise HTTPException(status_code=400, detail="Document appears to be empty or too short")
        job_id = str(uuid.uuid4())
        jobs_store[job_id] = {
            "job_id": job_id,
            "status": "uploaded",
            "document_name": file.filename,
            "text": text,
            "uploaded_at": datetime.now().isoformat()
        }
        logger.info(f"Document uploaded: {file.filename} (job_id={job_id})")
        return JSONResponse(content={
            "job_id": job_id,
            "message": "Document uploaded successfully",
            "document_name": file.filename,
            "status": "uploaded"
        })
    except ValueError as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process upload: {str(e)}")

@router.post("/analyze")
async def analyze_document(request: AnalysisRequest, background_tasks: BackgroundTasks):
    job_id = request.job_id
    if job_id not in jobs_store:
        logger.warning(f"Analyze failed: job_id {job_id} not found.")
        raise HTTPException(status_code=404, detail="Job ID not found")
    job = jobs_store[job_id]
    if job["status"] in ["processing", "completed"]:
        logger.warning(f"Analyze failed: job_id {job_id} is already {job['status']}.")
        raise HTTPException(status_code=400, detail=f"Job is already {job['status']}")
    text = job.get("text")
    document_name = job.get("document_name")
    if not text:
        logger.warning(f"Analyze failed: job_id {job_id} has no text.")
        raise HTTPException(status_code=400, detail="Document text not found")
    background_tasks.add_task(run_multi_agent_analysis, job_id, text, document_name)
    logger.info(f"Analysis started for job_id {job_id}")
    return JSONResponse(content={
        "job_id": job_id,
        "message": "Analysis started",
        "status": "processing"
    })

async def run_multi_agent_analysis(job_id: str, text: str, document_name: str):
    start_time = time.time()
    try:
        jobs_store[job_id]["status"] = "processing"
        results = await asyncio.gather(
            summarizer_agent(text),
            entity_extractor_agent(text),
            sentiment_analyzer_agent(text),
            return_exceptions=True
        )
        summary = results[0] if not isinstance(results[0], Exception) else "Summary unavailable due to agent failure"
        entities = results[1] if not isinstance(results[1], Exception) else {
            "people": [], "organizations": [], "dates": [], "locations": []
        }
        sentiment = results[2] if not isinstance(results[2], Exception) else {
            "tone": "neutral", "confidence": 0.0
        }
        processing_time = time.time() - start_time
        jobs_store[job_id] = {
            "job_id": job_id,
            "status": "completed",
            "document_name": document_name,
            "results": {
                "summary": summary,
                "entities": entities,
                "sentiment": sentiment
            },
            "processing_time_seconds": round(processing_time, 2)
        }
        failures = []
        if isinstance(results[0], Exception):
            failures.append(f"Summarizer: {str(results[0])}")
        if isinstance(results[1], Exception):
            failures.append(f"Entity Extractor: {str(results[1])}")
        if isinstance(results[2], Exception):
            failures.append(f"Sentiment Analyzer: {str(results[2])}")
        if failures:
            jobs_store[job_id]["agent_failures"] = failures
    except Exception as e:
        jobs_store[job_id] = {
            "job_id": job_id,
            "status": "failed",
            "document_name": document_name,
            "error": str(e),
            "processing_time_seconds": round(time.time() - start_time, 2)
        }

@router.get("/results/{job_id}")
async def get_results(job_id: str):
    if job_id not in jobs_store:
        logger.warning(f"Get results failed: job_id {job_id} not found.")
        raise HTTPException(status_code=404, detail="Job ID not found")
    job = jobs_store[job_id]
    response = {k: v for k, v in job.items() if k != "text"}
    logger.info(f"Results retrieved for job_id {job_id}")
    return JSONResponse(content=response)

@router.get("/")
async def root():
    return {
        "message": "Multi-Agent Document Analysis System (Gemini)",
        "version": "1.0.0",
        "llm_provider": "Google Gemini",
        "endpoints": {
            "POST /upload": "Upload a document (PDF/TXT)",
            "POST /analyze": "Start analysis on uploaded document",
            "GET /results/{job_id}": "Get analysis results"
        }
    }

@router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
