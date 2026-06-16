from fastapi import FastAPI
from app.api.v1 import auth, job_descriptions, resumes

app = FastAPI(title="Resume Screener API")

app.include_router(auth.router)
app.include_router(job_descriptions.router)
app.include_router(resumes.router)

@app.get("/")
async def root():
    return {"status": "ok"}