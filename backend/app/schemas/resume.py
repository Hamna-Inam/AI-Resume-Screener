from pydantic import BaseModel
import uuid
from datetime import datetime

class ResumeCreate(BaseModel):
    job_description_id: uuid.UUID
    candidate_name: str
    resume_text: str

class ResumeResponse(BaseModel):
    id: uuid.UUID
    job_description_id: uuid.UUID
    submitted_by: uuid.UUID
    candidate_name: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}