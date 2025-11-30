from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ResumeIn, ResumeOut
from app import utils
from app.llm_client import extract_resume_with_llm  # will raise if GEMINI_API_KEY missing

app = FastAPI(title="Resume Screener", version="0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Use POST /screen-resume or /screen-resume-llm"}

@app.post("/screen-resume", response_model=ResumeOut)
def screen_resume(payload: ResumeIn):
    text = payload.resume_text or ""
    if len(text.strip()) < 10:
        raise HTTPException(status_code=400, detail="resume_text is empty or too short")

    name = utils.extract_name(text)
    tech_stack = utils.extract_tech_stack(text)
    years = utils.calculate_years(text)
    score, matched = utils.compute_fit_score(tech_stack)

    return {
        "extraction": {"name": name, "tech_stack": tech_stack},
        "calculation": {"estimated_years_experience": years},
        "scoring": {"fit_score": score, "matched_skills": matched},
        "raw_text": None
    }

@app.post("/screen-resume-llm", response_model=ResumeOut)
def screen_resume_llm(payload: ResumeIn):
    text = payload.resume_text or ""
    if len(text.strip()) < 20:
        raise HTTPException(status_code=400, detail="resume_text is empty or too short")
    try:
        result = extract_resume_with_llm(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    # normalize and return
    extraction = result.get("extraction", {})
    calculation = result.get("calculation", {})
    scoring = result.get("scoring", {})

    return {
        "extraction": {"name": extraction.get("name"), "tech_stack": extraction.get("tech_stack", [])},
        "calculation": {"estimated_years_experience": float(calculation.get("estimated_years_experience", 0.0))},
        "scoring": {"fit_score": float(scoring.get("fit_score", 0.0)), "matched_skills": scoring.get("matched_skills", [])},
        "raw_text": None
    }
