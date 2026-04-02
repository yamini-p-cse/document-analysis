from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum

class SentimentEnum(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class AnalysisResult(BaseModel):
    summary: str
    entities: Dict[str, List[str]]
    sentiment: SentimentEnum
    confidence: float
    raw_text: Optional[str] = None

class ProcessResponse(BaseModel):
    success: bool
    filename: str
    analysis: AnalysisResult
    processing_time: float