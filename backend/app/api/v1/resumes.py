from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.schemas.resume import ResumeCreate, ResumeResponse

router = APIRouter(prefix="/v1/resumes", tags=["resumes"])


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def submit_resume(
    payload: ResumeCreate,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(JobDescription.id == payload.job_description_id)
    )
    jd = result.scalar_one_or_none()

    if jd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    new_resume = Resume(
        job_description_id=payload.job_description_id,
        submitted_by=current_user.id,
        candidate_name=payload.candidate_name,
        resume_text=payload.resume_text,
        status="pending",
    )
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    # TODO: enqueue Celery task here once workers are set up

    return new_resume


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: uuid.UUID,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    return resume