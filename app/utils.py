import re
from datetime import datetime
from typing import List, Optional, Tuple

TECH_KEYWORDS = [
    "python","java","c++","c#","javascript","nodejs","node","react",
    "angular","vue","fastapi","flask","django","pytorch","tensorflow",
    "keras","sklearn","pandas","numpy","sql","postgres","mysql","mongodb",
    "docker","kubernetes","aws","gcp","azure","nlp","spark","hadoop"
]

DATE_RANGE_RE = re.compile(
    r'(?P<start>\b(19|20)\d{2})\s*(?:-|to|–|—)\s*(?P<end>Present\b|\b(19|20)\d{2})',
    flags=re.IGNORECASE
)

def extract_name(text: str) -> Optional[str]:
    for line in text.splitlines()[:8]:
        line = line.strip()
        if not line:
            continue
        if any(tok in line.lower() for tok in ("@", "http", "linkedin", "www", "resume")):
            continue
        words = line.split()
        if 1 < len(words) <= 4 and all(w[0].isupper() for w in words if w):
            if any(ch.isdigit() for ch in line):
                continue
            if any(t.lower() in line.lower() for t in ("engineer","manager","intern","developer","consultant","director","analyst","student")):
                parts = re.split(r'[-,–—]', line)
                candidate = parts[0].strip()
                if 1 < len(candidate.split()) <= 4 and all(w[0].isupper() for w in candidate.split()):
                    return candidate
                continue
            return line
    return None

def extract_tech_stack(text: str) -> List[str]:
    t = text.lower()
    found = []
    for kw in TECH_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', t):
            found.append(kw)
    return sorted(set(found))

def calculate_years(text: str) -> float:
    now_year = datetime.now().year
    total_years = 0.0
    found_any = False
    for m in DATE_RANGE_RE.finditer(text):
        found_any = True
        start = int(m.group("start"))
        end_group = m.group("end")
        if re.search(r'present', end_group, re.I):
            end = now_year
        else:
            end = int(re.sub(r'\D', '', end_group))
        years = max(0, end - start)
        total_years += years
    if not found_any:
        years_all = [int(y) for y in re.findall(r'\b((?:19|20)\d{2})\b', text)]
        if years_all:
            try:
                span = max(years_all) - min(years_all)
                total_years = float(span)
            except:
                total_years = 0.0
    return round(total_years, 1)

def compute_fit_score(techs: List[str], desired_skills: Optional[List[str]] = None) -> Tuple[float, List[str]]:
    if desired_skills is None:
        desired_skills = ["python","fastapi","pytorch","tensorflow","sql","docker","aws"]
    matched = [t for t in desired_skills if t in techs]
    weights = {s: (2.0 if s == "python" else 1.0) for s in desired_skills}
    score_raw = sum(weights[s] for s in matched)
    max_raw = sum(weights.values())
    normalized = (score_raw / max_raw) * 10.0 if max_raw > 0 else 0.0
    bonus = max(0, len([t for t in techs if t not in desired_skills]) * 0.2)
    final = round(min(10.0, normalized + bonus), 1)
    return final, matched
