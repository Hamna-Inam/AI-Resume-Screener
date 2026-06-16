from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.models.job_description import JobDescription
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionResponse

router = APIRouter(prefix="/v1/job-descriptions", tags=["job descriptions"])


@router.post("", response_model=JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_job_description(
    payload: JobDescriptionCreate,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    new_jd = JobDescription(
        created_by=current_user.id,
        title=payload.title,
        description=payload.description,
    )
    db.add(new_jd)
    await db.commit()
    await db.refresh(new_jd)
    return new_jd


@router.get("", response_model=list[JobDescriptionResponse])
async def list_job_descriptions(
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(JobDescription))
    return result.scalars().all()


@router.get("/{jd_id}", response_model=JobDescriptionResponse)
async def get_job_description(
    jd_id: uuid.UUID,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(JobDescription).where(JobDescription.id == jd_id))
    jd = result.scalar_one_or_none()

    if jd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    return jd