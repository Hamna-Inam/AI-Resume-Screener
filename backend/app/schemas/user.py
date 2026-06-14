from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "recruiter"

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str