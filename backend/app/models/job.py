from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    recruiter_id = Column(Integer, ForeignKey("users.id"))