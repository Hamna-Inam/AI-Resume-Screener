# AI-Resume-Screener

An AI-powered resume screening system with async job queuing, JWT authentication
with RBAC, PostgreSQL, versioned REST APIs, and a React dashboard.

## Tech Stack

**Backend** — FastAPI, SQLAlchemy, PostgreSQL, Celery, Redis, Gemini API  
**Frontend** — React  
**Infra** — Docker Compose, GitHub Actions, AWS EC2  

## Architecture

<img width="658" height="516" alt="image" src="https://github.com/user-attachments/assets/aa672477-f1a1-4f93-a35b-bb036b3ef7ab" />


## Database Schema
<img width="193" height="589" alt="image" src="https://github.com/user-attachments/assets/45043676-8446-492b-8c41-d2bec01cb7b8" />


### Tables
- **users** — stores recruiters and admins with bcrypt-hashed passwords and role-based access
- **job_descriptions** — JDs created by recruiters
- **resumes** — one row per resume submitted against a JD, tracks processing status
- **screening_results** — AI-generated output per resume (score, strengths, gaps, recommendation)

## Progress

- [x] Project structure
- [x] Docker Compose setup (postgres, redis, backend, celery worker)
- [x] Core config with pydantic-settings
- [x] Async database setup with connection pooling
- [x] JWT + bcrypt security utilities
- [x] SQLAlchemy models
- [x] Pydantic schemas
- [x] Auth routes (register, login) with JWT
- [x] `get_current_user` + `require_role` (RBAC) dependencies
- [x] Job description routes (create, list, get by id)
- [x] Resume submission route with FK validation against job descriptions
- [x] Celery tasks
- [x] WebSockets
- [ ] CI/CD pipeline
- [ ] AWS deployment
- [x] Pytest test suite (auth, RBAC, duplicate handling)
- [x] GitHub Actions CI pipeline (tests + Docker build on every push)

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/resume-screener
cd resume-screener
cp .env.example .env  # add your keys
docker compose up --build
```
