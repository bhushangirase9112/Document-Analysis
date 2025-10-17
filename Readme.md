
**Maintainer:** Bhushan Girase
# Multi-Agent Document Analysis System 

A modular FastAPI application for document upload, summarization, entity extraction, and sentiment analysis using Google Gemini.

## Features
- Upload PDF or TXT documents
- Summarize content using Gemini LLM
- Extract people, organizations, dates, and locations
- Analyze sentiment (positive, negative, neutral)
- Modular codebase with logging and best practices

## Project Structure
```
.
├── agents.py         # LLM agent logic (summarizer, entity extractor, sentiment analyzer)
├── main.py           # FastAPI app startup and configuration
├── models.py         # Pydantic models
├── requirements.txt  # Python dependencies
├── routes.py         # API endpoints
├── utils.py          # PDF/text extraction utilities
└── README.md         # This file
```

## Setup Instructions

1. **Clone the repository**
   ```
   git clone https://github.com/bhushangirase9112/Document-Analysis.git
   cd Document-Analysis
   ```
2. **Create and activate a virtual environment (Windows):**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your_google_gemini_api_key_here
     ```
5. **Run the FastAPI server:**
   ```
   python main.py
   ```
   The server will start at http://127.0.0.1:8000

---

## API Documentation

### 1. Upload Document
- **Endpoint:** `POST /upload`
- **Description:** Upload a PDF or TXT document for analysis.
- **Request:**
  - Content-Type: `multipart/form-data`
  - Form field: `file` (PDF or TXT)
- **Response:**
  - `job_id`: Unique ID for the uploaded document
  - `status`: Upload status

### 2. Start Analysis
- **Endpoint:** `POST /analyze`
- **Description:** Start multi-agent analysis on an uploaded document.
- **Request Body:**
  ```json
  { "job_id": "<job_id_from_upload>" }
  ```
- **Response:**
  - `job_id`: Job ID
  - `status`: Processing status

### 3. Get Results
- **Endpoint:** `GET /results/{job_id}`
- **Description:** Retrieve analysis results for a document.
- **Response:**
  - `summary`: Document summary
  - `entities`: Extracted people, organizations, dates, locations
  - `sentiment`: Sentiment analysis result

---

## Design Decisions

**1. Modular Structure:**
The project is split into logical modules: `main.py` (app startup), `routes.py` (API endpoints), `agents.py` (LLM agent logic),  `utils.py` (PDF/text extraction), and `models.py` (Pydantic models). This separation improves maintainability, testability, and clarity.

**2. FastAPI & Async:**
FastAPI was chosen for its speed, async support, and automatic OpenAPI docs. All endpoints and agent calls are async, allowing concurrent processing and better scalability.

**3. Google Gemini Integration:**
The Gemini LLM is used for summarization, entity extraction, and sentiment analysis. Prompts are crafted for each agent, and the API key is loaded from a `.env` file for security.

**4. In-Memory Job Store:**
A simple in-memory dictionary is used to track jobs and results. This is suitable for prototyping and local use.

**5. Logging:**
Python's logging module is configured in all modules for info, warning, and error logs. This aids debugging and monitoring in development.

**6. Error Handling:**
All endpoints and agents have try/except blocks to catch and log errors, returning clear HTTP error responses. This prevents server crashes and provides useful feedback to API consumers.

**7. Extensibility:**
The modular design allows easy addition of new agents, endpoints, or storage backends. Prompts and logic can be customized in `agents.py` without affecting the API layer.

**8. Security:**
CORS is enabled for all origins for demo purposes. 

---




