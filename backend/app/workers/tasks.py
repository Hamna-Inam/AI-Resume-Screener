from celery import Celery
import asyncio
import redis.asyncio as redis
import json

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.screening_result import ScreeningResult
from app.services.ai_service import screen_resume

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)


@celery_app.task(name="screen_resume_task")
def screen_resume_task(resume_id: str):
    asyncio.run(_screen_resume_async(resume_id))

async def _screen_resume_async(resume_id: str):
    engine = create_async_engine(settings.DATABASE_URL, poolclass=None)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    redis_client = redis.from_url(settings.REDIS_URL)
    channel_name = f"resume_status:{resume_id}"

    async def publish_status(status: str, result: dict | None = None):
        payload = {"resume_id": resume_id, "status": status}
        if result:
            payload["result"] = result
        await redis_client.publish(channel_name, json.dumps(payload))

    async with SessionLocal() as db:
        result = await db.execute(select(Resume).where(Resume.id == resume_id))
        resume = result.scalar_one_or_none()
        if resume is None:
            await redis_client.close()
            await engine.dispose()
            return

        resume.status = "processing"
        await db.commit()
        await publish_status("processing")

        jd_result = await db.execute(
            select(JobDescription).where(JobDescription.id == resume.job_description_id)
        )
        jd = jd_result.scalar_one_or_none()

        try:
            ai_output = await screen_resume(resume.resume_text, jd.description)

            screening_result = ScreeningResult(
                resume_id=resume.id,
                match_score=ai_output["match_score"],
                strengths=ai_output["strengths"],
                gaps=ai_output["gaps"],
                recommendation=ai_output["recommendation"],
            )
            db.add(screening_result)
            resume.status = "completed"
            await db.commit()
            await publish_status("completed", ai_output)

        except Exception as e:
            resume.status = "failed"
            await db.commit()
            await publish_status("failed")
            print(f"Screening failed for resume {resume_id}: {e}")

    await redis_client.close()
    await engine.dispose()