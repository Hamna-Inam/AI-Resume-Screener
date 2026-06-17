import json
import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SCREENING_PROMPT = """You are a technical recruiter. Compare this resume against the job description.

Job description:
{job_description}

Resume:
{resume_text}

Respond ONLY with valid JSON in this exact format, no other text:
{{
  "match_score": <integer 0-100>,
  "strengths": "<2-3 sentences on what matches well>",
  "gaps": "<2-3 sentences on what's missing>",
  "recommendation": "<one sentence: strong match / moderate match / weak match, and why>"
}}"""


async def screen_resume(resume_text: str, job_description: str) -> dict:
    prompt = SCREENING_PROMPT.format(
        job_description=job_description,
        resume_text=resume_text,
    )

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    raw_text = raw_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    return json.loads(raw_text)