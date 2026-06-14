from pydantic import BaseModel
import uuid
from datetime import datetime

class ScreeningResultResponse(BaseModel):
    id: uuid.UUID
    resume_id: uuid.UUID
    match_score: int
    strengths: str
    gaps: str
    recommendation: str
    created_at: datetime

    model_config = {"from_attributes": True}