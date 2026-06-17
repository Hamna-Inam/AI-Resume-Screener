from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid

from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.screening_result import ScreeningResult
from app.schemas.screening_result import ScreeningResultResponse
from typing import Optional
from app.schemas.resume import ResumeResponse
from app.services.file_parser import extract_text_from_file

router = APIRouter(prefix="/v1/resumes", tags=["resumes"])


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def submit_resume(
    job_description_id: uuid.UUID = Form(...),
    candidate_name: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(JobDescription.id == job_description_id)
    )
    jd = result.scalar_one_or_none()
    if jd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    file_bytes = await file.read()
    try:
        resume_text = extract_text_from_file(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract any text from the uploaded file",
        )

    new_resume = Resume(
        job_description_id=job_description_id,
        submitted_by=current_user.id,
        candidate_name=candidate_name,
        resume_text=resume_text,
        status="pending",
    )
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    from app.workers.tasks import screen_resume_task
    screen_resume_task.delay(str(new_resume.id))

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

@router.get("/{resume_id}/result", response_model=ScreeningResultResponse)
async def get_screening_result(
    resume_id: uuid.UUID,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ScreeningResult).where(ScreeningResult.resume_id == resume_id)
    )
    screening_result = result.scalar_one_or_none()

    if screening_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening result not found — resume may still be processing",
        )

    return screening_result




@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    search: Optional[str] = None,
    min_score: Optional[int] = None,
    job_description_id: Optional[uuid.UUID] = None,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Resume)

    if current_user.role == "recruiter":
        query = query.where(Resume.submitted_by == current_user.id)

    if search:
        query = query.where(Resume.candidate_name.ilike(f"%{search}%"))

    if job_description_id:
        query = query.where(Resume.job_description_id == job_description_id)

    if min_score is not None:
        query = query.join(ScreeningResult, ScreeningResult.resume_id == Resume.id)
        query = query.where(ScreeningResult.match_score >= min_score)

    result = await db.execute(query)
    return result.scalars().all()