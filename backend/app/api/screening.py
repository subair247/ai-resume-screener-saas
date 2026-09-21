from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import re
from backend.app.core.database import get_db
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job  
from backend.app.schemas.screening_schema import JobCreate
from backend.app.services.nlp_pipeline import get_embedding
from backend.app.services.faiss_index import faiss_db
from backend.app.services.ai_service import generate_interview_questions
from backend.app.services.email_service import send_interview_questions_email

router = APIRouter(prefix="/screening", tags=["Screening & Ranking"])

@router.post("/match")
def match_candidates(job: JobCreate, db: Session = Depends(get_db)):
    job_embedding = get_embedding(job.description)
    results = faiss_db.search(job_embedding, k=5)
    
    ranked_candidates = []
    for res in results:
        meta = res["meta"]
        distance = res["distance"]
        candidate = db.query(Candidate).filter(Candidate.id == meta["candidate_id"]).first()
        if candidate:
            score = 1.0 / (1.0 + distance)
            candidate.score = score
            db.commit()
            
            job_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', job.description.lower()))
            candidate_text = (candidate.skills + " " + candidate.resume_text).lower()
            missing = [word for word in job_words if word not in candidate_text][:5]
            
            ranked_candidates.append({
                "candidate_id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "score": round(score * 100, 2),
                "skills": candidate.skills.split(", ") if candidate.skills else [],
                "missing_keywords": missing,
                "recommendation": f"Add missing key terms like: {', '.join(missing)} to boost your score!" if missing else "Profile looks solid!"
            })
            
    ranked_candidates.sort(key=lambda x: x["score"], reverse=True)
    return {"matched_candidates": ranked_candidates}


@router.post("/generate-questions/{candidate_id}")
def get_candidate_questions(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    try:
        questions = generate_interview_questions(job.description, candidate.resume_text)
        return {"candidate_id": candidate.id, "candidate_name": candidate.name, "interview_questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-questions-email/{candidate_id}")
def send_questions_email(candidate_id: int, job_id: int = Query(...), email: str = Query(...), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    try:
        questions = generate_interview_questions(job.description, candidate.resume_text)
        success = send_interview_questions_email(email, candidate.name, questions)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email via SMTP")
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))