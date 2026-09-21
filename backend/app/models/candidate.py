from sqlalchemy import Column, Integer, String, Text, Float
from backend.app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    skills = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True)
    score = Column(Float, default=0.0)