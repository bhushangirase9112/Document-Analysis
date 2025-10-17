import asyncio
import json
from google.generativeai import GenerativeModel
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Configure logging
import logging
logger = logging.getLogger(__name__)

# # The model instance will be injected from main.py
# model: GenerativeModel = None

# def set_model(m):
#     global model
#     model = m
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")
logger.info(f"Model configured: {model}")


async def summarizer_agent(text: str) -> str:
    try:
        logger.info("Summarizer agent started.")
        prompt = f"""Create a concise summary of the following document in maximum 150 words. \nFocus on key points and main ideas.\n\nDocument:\n{text[:4000]}"""
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=2000
            )
        )
        summary_text = getattr(response, 'text', None)
        if summary_text and summary_text.strip():
            logger.info("Summarizer agent completed successfully.")
            return summary_text.strip()
        else:
            logger.warning("Summarizer agent: Gemini model did not return any output.")
            return "Summary unavailable: Gemini model did not return any output."
    except Exception as e:
        logger.error(f"Summarizer agent failed: {str(e)}")
        raise Exception(f"Summarizer agent failed: {str(e)}")
    





async def entity_extractor_agent(text: str) -> Dict[str, List[str]]:
    try:
        logger.info("Entity extractor agent started.")
        prompt = f"""Extract the following entities from the text:\n- People (names of individuals)\n- Organizations (companies, institutions)\n- Dates (specific dates mentioned)\n- Locations (cities, countries, places)\n\nReturn ONLY a JSON object with these exact keys: people, organizations, dates, locations. \nEach value should be a list of strings. If no entities found for a category, return an empty list.\n\nDocument:\n{text[:4000]}\n\nResponse (JSON only):"""
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1
            )
        )
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        entities = json.loads(response_text.strip())
        logger.info("Entity extractor agent completed successfully.")
        return {
            "people": entities.get("people", []),
            "organizations": entities.get("organizations", []),
            "dates": entities.get("dates", []),
            "locations": entities.get("locations", [])
        }
    except Exception as e:
        logger.error(f"Entity extractor agent failed: {str(e)}")
        raise Exception(f"Entity extractor agent failed: {str(e)}")
    





async def sentiment_analyzer_agent(text: str) -> Dict[str, any]:
    try:
        logger.info("Sentiment analyzer agent started.")
        prompt = f"""Analyze the sentiment/tone of the following document and determine if it's positive, negative, or neutral. \nAlso provide a confidence score between 0 and 1.\n\nReturn ONLY a JSON object with these exact keys:\n- tone: one of \"positive\", \"negative\", or \"neutral\"\n- confidence: a float between 0 and 1\n\nDocument:\n{text[:4000]}\n\nResponse (JSON only):"""
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1
            )
        )
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        sentiment = json.loads(response_text.strip())
        logger.info("Sentiment analyzer agent completed successfully.")
        return {
            "tone": sentiment.get("tone", "neutral"),
            "confidence": float(sentiment.get("confidence", 0.5))
        }
    except Exception as e:
        logger.error(f"Sentiment analyzer agent failed: {str(e)}")
        raise Exception(f"Sentiment analyzer agent failed: {str(e)}")
