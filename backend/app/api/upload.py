from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import os
import re
import spacy
from app.core.database import get_db
from app.models.candidate import Candidate
from app.services.parser import parse_pdf, parse_docx
from app.services.nlp_pipeline import extract_entities, get_embedding
from app.services.faiss_index import faiss_db

router = APIRouter(prefix="/upload", tags=["Upload & Parsing"])

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = file.filename.split(".")[-1].lower()
    temp_path = f"temp_{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        if ext == "pdf":
            text = parse_pdf(temp_path)
        elif ext == "docx":
            text = parse_docx(temp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    skills = extract_entities(text)
    embedding = get_embedding(text)
    
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text[:1000])
    candidate_name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            candidate_name = ent.text
            break
            
    if not candidate_name:
        clean_name = os.path.splitext(file.filename)[0]
        candidate_name = re.sub(r'[^a-zA-Z\s]', ' ', clean_name).strip()
        
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    candidate_email = email_match.group(0) if email_match else "not_found@domain.com"
    existing_candidate = db.query(Candidate).filter(Candidate.email == candidate_email).first()
    
    if existing_candidate:
        existing_candidate.name = candidate_name
        existing_candidate.skills = ", ".join(skills)
        existing_candidate.resume_text = text
        db.commit()
        db.refresh(existing_candidate)
        
        candidate_id = existing_candidate.id
        message = "Resume updated successfully (Duplicate entry handled)"
    else:
        candidate = Candidate(
            name=candidate_name,
            email=candidate_email,
            skills=", ".join(skills),
            resume_text=text
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        
        candidate_id = candidate.id
        message = "Resume uploaded and processed successfully"
    
    faiss_db.add_vector(embedding, {"candidate_id": candidate_id, "name": candidate_name})
    
    return {
        "message": message, 
        "candidate_id": candidate_id, 
        "name": candidate_name, 
        "skills": skills
    }