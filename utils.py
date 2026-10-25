import re
import io
import os
import json
import anthropic
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    import pdfplumber
    PDF_OK = True
except ImportError:
    PDF_OK = False

# ─────────────────────────────────────────────────────────────
#  ROLE SKILLS DATABASE
# ─────────────────────────────────────────────────────────────
ROLE_SKILLS = {
    "Software Engineer": [
        "python", "java", "c++", "javascript", "typescript", "react", "angular", "vue",
        "node.js", "sql", "mongodb", "postgresql", "redis", "api", "rest", "graphql",
        "git", "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "system design",
        "data structures", "algorithms", "oop", "microservices", "html", "css", "linux"
    ],
    "Data Analyst": [
        "sql", "excel", "python", "tableau", "power bi", "looker", "statistics",
        "data visualization", "pandas", "numpy", "dashboard", "reporting", "kpi",
        "business analysis", "etl", "data cleaning", "pivot tables", "vlookup",
        "a/b testing", "google analytics", "bigquery", "snowflake", "dbt"
    ],
    "Data Scientist": [
        "python", "machine learning", "deep learning", "sql", "pandas", "numpy",
        "scikit-learn", "tensorflow", "pytorch", "xgboost", "statistics",
        "data visualization", "feature engineering", "nlp", "computer vision",
        "model deployment", "mlflow", "airflow", "spark", "a/b testing",
        "bayesian inference", "time series", "experimentation"
    ],
    "Product Manager": [
        "product roadmap", "user research", "wireframing", "agile", "scrum",
        "jira", "confluence", "stakeholder management", "data analysis", "sql",
        "a/b testing", "go-to-market", "user stories", "okrs", "kpis",
        "competitive analysis", "product strategy", "customer discovery",
        "prioritization", "figma", "metrics", "growth"
    ],
    "ML Engineer": [
        "python", "machine learning", "tensorflow", "pytorch", "mlops", "docker",
        "kubernetes", "aws sagemaker", "model serving", "feature store", "airflow",
        "spark", "data pipelines", "model monitoring", "ci/cd", "api", "fastapi",
        "triton", "ray", "distributed training", "inference optimization", "onnx"
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "terraform", "ansible", "jenkins", "github actions",
        "aws", "gcp", "azure", "linux", "bash", "python", "monitoring", "grafana",
        "prometheus", "elk stack", "ci/cd", "helm", "networking", "security",
        "infrastructure as code", "site reliability", "incident management"
    ],
    "Frontend Developer": [
        "javascript", "typescript", "react", "vue", "angular", "html", "css",
        "sass", "tailwind", "webpack", "vite", "redux", "graphql", "rest api",
        "responsive design", "accessibility", "testing", "jest", "cypress",
        "performance optimization", "figma", "git", "node.js", "next.js"
    ],
    "Backend Developer": [
        "python", "java", "go", "node.js", "sql", "postgresql", "mongodb",
        "redis", "rest api", "graphql", "microservices", "docker", "aws",
        "message queues", "kafka", "rabbitmq", "authentication", "authorization",
        "caching", "database design", "orm", "git", "linux", "system design"
    ],
    "UX Designer": [
        "figma", "sketch", "adobe xd", "user research", "wireframing", "prototyping",
        "usability testing", "information architecture", "design systems", "accessibility",
        "interaction design", "visual design", "user interviews", "personas",
        "journey mapping", "html", "css", "invision", "zeplin", "miro"
    ],
    "Cybersecurity Analyst": [
        "network security", "penetration testing", "vulnerability assessment", "siem",
        "incident response", "firewalls", "ids/ips", "python", "linux", "splunk",
        "threat intelligence", "malware analysis", "risk assessment", "compliance",
        "iso 27001", "nist", "owasp", "cloud security", "ethical hacking", "cryptography"
    ],
}

# ─────────────────────────────────────────────────────────────
#  TEXT & PDF UTILS
# ─────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def extract_pdf_text(uploaded_file) -> tuple[str | None, str | None]:
    if not PDF_OK:
        return None, "Install pdfplumber: pip install pdfplumber"
    try:
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        return text.strip(), None
    except Exception as e:
        return None, str(e)

# ─────────────────────────────────────────────────────────────
#  SCORING
# ─────────────────────────────────────────────────────────────
def calculate_match_tfidf(resume: str, jd: str) -> int:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform([resume.lower(), jd.lower()])
        sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return min(int(sim * 100 * 1.6), 100)
    except Exception:
        return 0

def find_keyword_gaps(resume: str, jd: str) -> tuple[list, list]:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform([resume.lower(), jd.lower()])
        features = vectorizer.get_feature_names_out()
        r_vec, j_vec = matrix.toarray()[0], matrix.toarray()[1]
        missing, matched = [], []
        for word, r, j in zip(features, r_vec, j_vec):
            if j > 0 and r == 0:   missing.append((word, j))
            elif j > 0 and r > 0:  matched.append(word)
        missing.sort(key=lambda x: -x[1])
        return [w for w, _ in missing[:22]], matched[:22]
    except Exception:
        return [], []

def find_role_skill_gaps(resume_text: str, role: str) -> tuple[list, list]:
    rl = resume_text.lower()
    skills = ROLE_SKILLS.get(role, [])
    return (
        [s for s in skills if s.lower() in rl],
        [s for s in skills if s.lower() not in rl],
    )

# ─────────────────────────────────────────────────────────────
#  READINESS / COLOUR HELPERS
# ─────────────────────────────────────────────────────────────
def get_readiness(score: int) -> tuple[str, str, str]:
    """Returns (label, color_key, message)"""
    if score >= 82:
        return (
            "Interview Ready",
            "green",
            "You have strong alignment with this role. Focus on polishing your story — you're in great shape.",
        )
    if score >= 65:
        return (
            "On the Right Track",
            "amber",
            "Solid foundations. A few targeted additions will make you significantly more competitive.",
        )
    if score >= 40:
        return (
            "Room to Grow",
            "amber",
            "Great starting point. Focused improvements here will transform your profile's impact.",
        )
    return (
        "Let's Build Your Edge",
        "violet",
        "Every expert started exactly here. Your personalised plan below will get you to the top.",
    )

def score_color_class(score: int) -> str:
    if score >= 75: return "col-g"
    if score >= 50: return "col-a"
    return "col-v"

def prog_gradient(score: int) -> str:
    if score >= 75: return "linear-gradient(90deg,#10b981,#059669)"
    if score >= 50: return "linear-gradient(90deg,#f59e0b,#d97706)"
    return                 "linear-gradient(90deg,#8b5cf6,#7c3aed)"

def banner_cls(color_key: str) -> tuple[str, str]:
    return {
        "green":  ("sb-green",  "✦"),
        "amber":  ("sb-amber",  "◈"),
        "violet": ("sb-violet", "◉"),
    }.get(color_key, ("sb-violet", "◉"))

# ─────────────────────────────────────────────────────────────
#  AI FEEDBACK
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    return anthropic.Anthropic(api_key=api_key) if api_key else None

def get_ai_feedback(
    resume_text: str,
    jd: str,
    role: str,
    matched_s: list,
    missing_s: list,
    missing_kw: list,
    score: int,
) -> tuple[dict | None, str | None]:
    client = get_client()
    if not client:
        return None, "Set ANTHROPIC_API_KEY to unlock AI coaching."

    prompt = f"""You are an enthusiastic, expert career coach specialising in {role} hiring.
Analyse this resume vs job description and deliver specific, actionable, POSITIVELY-FRAMED coaching.
Treat every gap as an exciting opportunity. Never use failure language.

TARGET ROLE: {role}
MATCH SCORE: {score}%
STRENGTHS PRESENT: {', '.join(matched_s[:10]) if matched_s else 'None detected'}
SKILLS TO HIGHLIGHT MORE: {', '.join(missing_s[:10]) if missing_s else 'None'}
TOP KEYWORDS TO ADD: {', '.join(missing_kw[:10]) if missing_kw else 'None'}

RESUME (first 2000 chars): {resume_text[:2000]}
JOB DESCRIPTION (first 1500 chars): {jd[:1500]}

Respond ONLY with pure JSON (no markdown, no code fences):
{{
  "executive_summary": "2-3 sharp sentences: what this candidate brings + their clearest opportunity",
  "biggest_strength": "The single most impressive, specific thing on this resume for this role",
  "growth_opportunity": "The ONE area where adding evidence creates maximum hiring uplift — frame it as an exciting next step",
  "ats_verdict": "One concrete sentence on keyword optimisation to reach more recruiters",
  "top_bullet_rewrite": {{
    "original_hint": "Description of a weak bullet pattern visible in the resume",
    "rewritten": "Powerful rewrite: Action Verb + specific metric + quantified business impact"
  }},
  "interview_prep": ["topic1", "topic2", "topic3", "topic4", "topic5"],
  "week_actions": ["Day 1 action", "Day 2 action", "Day 3 action", "Day 4 action", "Day 5 action", "Day 6 action", "Day 7 action"],
  "one_liner_pitch": "A confident, tailored 1-sentence opening pitch for interviews"
}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1400,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```json\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()
        return json.loads(raw), None
    except json.JSONDecodeError as e:
        return None, f"Could not parse AI response: {e}"
    except Exception as e:
        return None, f"AI error: {e}"