from pydantic import BaseModel, Field
from typing import List, Optional

class ResumeIn(BaseModel):
    resume_text: str = Field(..., example="John Doe\nSenior ML Engineer\nWorked at Acme Corp 2018 - 2020 ...\nSkills: Python, FastAPI")

class Extraction(BaseModel):
    name: Optional[str]
    tech_stack: List[str] = []

class Calculation(BaseModel):
    estimated_years_experience: float

class Scoring(BaseModel):
    fit_score: float
    matched_skills: List[str] = []

class ResumeOut(BaseModel):
    extraction: Extraction
    calculation: Calculation
    scoring: Scoring
    raw_text: Optional[str] = None
