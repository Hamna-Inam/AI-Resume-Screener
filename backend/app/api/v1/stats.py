from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.models.resume import Resume
from app.models.screening_result import ScreeningResult

router = APIRouter(prefix="/v1/stats", tags=["stats"])


@router.get("")
async def get_stats(
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: AsyncSession = Depends(get_db),
):
    base_query = select(Resume)
    if current_user.role == "recruiter":
        base_query = base_query.where(Resume.submitted_by == current_user.id)

    total_result = await db.execute(
        select(func.count()).select_from(base_query.subquery())
    )
    total_screened = total_result.scalar() or 0

    joined_query = (
        select(
            func.count(ScreeningResult.id),
            func.avg(ScreeningResult.match_score),
            func.sum(case((ScreeningResult.match_score >= 80, 1), else_=0)),
        )
        .join(Resume, Resume.id == ScreeningResult.resume_id)
    )
    if current_user.role == "recruiter":
        joined_query = joined_query.where(Resume.submitted_by == current_user.id)

    stats_result = await db.execute(joined_query)
    completed_count, avg_score, strong_matches = stats_result.one()

    return {
        "resumes_screened": total_screened,
        "strong_matches": strong_matches or 0,
        "avg_match_score": round(avg_score, 1) if avg_score else 0,
    }