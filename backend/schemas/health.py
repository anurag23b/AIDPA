# backend/schemas/health.py
from pydantic import BaseModel
from typing import List, Optional

class AnalyzeHealthRequest(BaseModel):
    data: str

class HealthRecord(BaseModel):
    steps: float
    heart_rate: float
    sleep_hours: float

class HealthInput(BaseModel):
    data: Optional[str] = None  # Make optional
    records: List[HealthRecord]

class HealthAnalysis(BaseModel):
    status: str
    recommendations: List[str]