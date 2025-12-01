# Resume Screening API (FastAPI)
The goal of this microservice is to analyze a raw resume text and return:

1. **Extraction** – Candidate Name & Tech Stack  
2. **Calculation** – Estimated Years of Experience  
3. **Scoring** – Fit Score (0–10) + Matched Skills  
4. **Optional** – LLM-powered extraction using **Gemini API** (Free Tier)

The API is built using **FastAPI**, and includes both:
- A **deterministic offline parser** (works without API keys)
- An **optional Gemini LLM endpoint** (requires `.env`)

---

## 🚀 Features

### 🔹 1. Extraction  
- Detects candidate name using heuristic rules  
- Extracts technical skills from a predefined dictionary

### 🔹 2. Experience Calculation  
- Parses date ranges like `2018-2020` or `2020–Present`  
- Sums experience duration across all ranges  
- Works even if only years are present in the text

### 🔹 3. Fit Score  
- Weighted scoring system (Python gets higher weight)  
- Rewards additional relevant technologies  
- Produces a normalized score between 0 and 10

### 🔹 4. Optional LLM Mode  
Uses **Gemini** to extract JSON-formatted resume insights.  
The `.env` file holds:



GEMINI_API_KEY=your_key_here


This endpoint is not required for reviewers to run the project.

---

## 🗂 Project Structure



.
├── app/
│ ├── main.py # FastAPI routes
│ ├── schemas.py # Pydantic models (input/output)
│ ├── utils.py # Deterministic extraction, scoring, experience calculation
│ └── llm_client.py # Gemini API wrapper (optional)
├── requirements.txt
├── .env.example # Shows required environment variable
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/ravisi89/Resume-Screening.git
cd Resume-Screening

2️⃣ Create virtual environment
python -m venv venv

3️⃣ Activate venv

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ (Optional) Enable LLM endpoint

Create .env in the root:

GEMINI_API_KEY=your_free_key_here


.env is ignored from GitHub for security.

▶️ Run the API
uvicorn app.main:app --reload --port 8000


Open Swagger UI:

http://127.0.0.1:8000/docs

🧪 Example Input
{
  "resume_text": "John Doe\nSenior ML Engineer\nAcme Corp 2018-2020; DataLabs 2020-Present\nSkills: Python, FastAPI, PyTorch, Docker, SQL"
}

📤 Example Output (Deterministic)
{
  "extraction": {
    "name": "John Doe",
    "tech_stack": ["python", "fastapi", "pytorch", "docker", "sql"]
  },
  "calculation": {
    "estimated_years_experience": 5.0
  },
  "scoring": {
    "fit_score": 9.2,
    "matched_skills": ["python", "fastapi", "pytorch"]
  }
}



