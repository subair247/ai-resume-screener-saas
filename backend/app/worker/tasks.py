from app.worker.celery_app import celery_app
from app.services.nlp_pipeline import get_embedding, extract_entities

@celery_app.task(name="process_resume_background")
def process_resume_background(file_text: str):
    skills = extract_entities(file_text)
    embedding = get_embedding(file_text)
    return {"status": "success", "skills_count": len(skills), "embedding_dim": len(embedding)}