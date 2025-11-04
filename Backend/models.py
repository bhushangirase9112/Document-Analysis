from pydantic import BaseModel
from typing import Dict, List, Optional

class AnalysisRequest(BaseModel):
    job_id: str


