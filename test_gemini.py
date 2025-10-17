from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import uuid
import time
from datetime import datetime
import PyPDF2
import io
import os
import json
import google.generativeai as genai
import uvicorn
from dotenv import load_dotenv


# Load environment variables from the .env file (if present)
load_dotenv()



api_key = os.getenv("GOOGLE_API_KEY")
print("Using API Key:", api_key)

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")



async def summarizer_agent(text: str) -> str:
    try:
        prompt = f"""Create a concise summary of the following document in maximum 150 words. 
Focus on key points and main ideas.

Document:
{text[:4000]}"""
        
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=200
            )
        )
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Summarizer agent failed: {str(e)}")
    
response = asyncio.run(summarizer_agent("This is a test document. It contains several sentences to demonstrate the summarization capabilities of the Gemini model. The goal is to extract the main points and present them in a concise manner. This document serves as an example for testing purposes."))
print(response)