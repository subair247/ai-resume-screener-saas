from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str

class ScreeningResponse(BaseModel):
    candidate_id: int
    name: str | None
    email: str | None
    score: float
    skills: list[str]