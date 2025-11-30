import os
import json
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
# model selection — recommended free model name may vary; use "gemini-pro" or consult docs
model = genai.GenerativeModel("gemini-pro")

def extract_resume_with_llm(resume_text: str) -> dict:
    prompt = f"""
You are a resume screening assistant.
Extract the following fields from the resume STRICTLY in JSON (no extra text):

{{
  "extraction": {{
    "name": null or "Full Name",
    "tech_stack": ["python","fastapi",...]
  }},
  "calculation": {{
    "estimated_years_experience": 0.0
  }},
  "scoring": {{
    "fit_score": 0.0,
    "matched_skills": []
  }}
}}

Resume:
\"\"\"{resume_text}\"\"\"

Return ONLY valid JSON.
"""
    response = model.generate_content(prompt)
    text = response.text
    try:
        return json.loads(text)
    except:
        s = text.find("{")
        e = text.rfind("}")
        return json.loads(text[s:e+1])
