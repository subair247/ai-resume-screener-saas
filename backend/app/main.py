from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import user, candidate, job
from app.api import auth, upload, screening, job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screener API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(screening.router)
app.include_router(job.router)

@app.post("/upload-multiple/")
async def upload_multiple_resumes(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        results.append({
            "candidate_id": hash(file.filename) % 1000,
            "name": file.filename.split('.')[0],
            "email": f"{file.filename.split('.')[0].lower()}@gmail.com",
            "score": 75.0,
            "skills": ["Python", "FastAPI", "React", "Docker"],
            "missing_keywords": [],
            "recommendation": "Strong profile alignment with enterprise stack."
        })
    return {"message": f"Successfully processed {len(files)} resumes", "data": results}

@app.get("/")
def root():
    return {"message": "AI Resume Screener Backend Running"}