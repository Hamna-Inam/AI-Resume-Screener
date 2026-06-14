from pydantic import BaseModel
import uuid
from datetime import datetime

class JobDescriptionCreate(BaseModel):
    title: str
    description: str

class JobDescriptionResponse(BaseModel):
    id: uuid.UUID
    created_by: uuid.UUID
    title: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}