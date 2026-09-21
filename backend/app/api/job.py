from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from backend.app.core.database import get_db
from backend.app.models.job import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobCreate(BaseModel):
    title: str
    description: str

class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True

class Config:
        from_attributes = True

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(title=job.title, description=job.description)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()