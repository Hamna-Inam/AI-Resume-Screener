from fastapi import FastAPI
from app.api.v1 import auth, job_descriptions, resumes, websockets, stats


app = FastAPI(title="Resume Screener API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(job_descriptions.router)
app.include_router(resumes.router)
app.include_router(websockets.router)
app.include_router(stats.router)



@app.get("/")
async def root():
    return {"status": "ok"}