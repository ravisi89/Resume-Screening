# Resume Screening / Sentiment Engine (Submission)

This repository contains two small FastAPI microservices built for the AI Engineering Intern technical assessment:

- **Sentiment Engine** (Option 1) — analyzes a batch of reviews and returns overall sentiment, top themes, and a one-line actionable feedback.
- **Resume Screener** (Option 2) — extracts name & tech stack, estimates years of experience, and produces a fit score for a Senior Python/AI role. Includes a deterministic endpoint (offline) and an optional LLM endpoint (Gemini) that can be enabled with a free key.

> Both services are deterministic and reproducible. The Sentiment Engine works fully offline. The Resume Screener provides both an offline heuristic endpoint and a Gemini-powered endpoint (optional).

---

## Repository structure



.
├── app/
│ ├── init.py
│ ├── main.py # FastAPI entry (two endpoints)
│ ├── schemas.py # Pydantic models
│ ├── utils.py # Deterministic helpers (extraction, years, scoring)
│ └── llm_client.py # Optional: Gemini LLM wrapper (disabled unless .env present)
├── requirements.txt
├── README.md
└── .env.example


---

## Quick start (run locally)

> Recommended: create a virtual environment and install dependencies.

```bash
# 1. clone
git clone https://github.com/ravisi89/Resume-Screening.git
cd Resume-Screening

# 2. create venv
python -m venv venv

# on Windows
venv\Scripts\activate

# on macOS/Linux
# source venv/bin/activate

# 3. install dependencies
pip install -r requirements.txt

# 4. (Optional) enable Gemini LLM endpoint:
# create a file named .env in the repo root (do NOT commit .env)
# and add:
# GEMINI_API_KEY=your_free_gemini_key_here

# 5. run the API
uvicorn app.main:app --reload --port 8000


Open the Swagger UI:

http://127.0.0.1:8000/docs

API endpoints
Sentiment Engine (example)

POST /analyze

Body:

{"reviews": ["I love the new feature, but the UI is too slow.", "Terrible support."]}


Response (example):

{
  "overall_sentiment": "negative",
  "sentiment_score": -0.44,
  "key_themes": ["ui","support","feature"],
  "actionable_feedback": "Improve ui, support to address customer concerns."
}

Resume Screener (deterministic, offline)

POST /screen-resume

Body:

{"resume_text": "John Doe\nSenior ML Engineer\nWorked at Acme 2018-2020; DataLabs 2020-Present\nSkills: Python, PyTorch, FastAPI, Docker"}


Response (example):

{
  "extraction": {"name":"John Doe","tech_stack":["python","pytorch","fastapi","docker"]},
  "calculation": {"estimated_years_experience": 5.0},
  "scoring": {"fit_score": 9.0,"matched_skills":["python","pytorch","fastapi"]}
}
