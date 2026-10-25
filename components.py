import streamlit as st

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:0.8rem 0 0.3rem;">
          <div class="sb-logo">✦ HireMe AI</div>
          <div class="sb-tagline">Your personal career coach</div>
        </div>
        <hr class="sb-rule">
        <div class="sb-section-lbl">How it works</div>
        """, unsafe_allow_html=True)

        steps = [
            "Upload or paste your resume",
            "Paste the full job description",
            "Choose your target role",
            "Hit Analyse — results in seconds",
        ]
        for i, s in enumerate(steps, 1):
            st.markdown(
                f'<div class="sb-step"><div class="sb-num">{i}</div><div>{s}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="sb-rule"><div class="sb-section-lbl">What you unlock</div>', unsafe_allow_html=True)
        features = [
            "TF-IDF match score",
            "Role-specific skill map",
            "ATS keyword intelligence",
            "Claude AI career coaching",
            "Live bullet rewrite",
            "Personalised 7-day plan",
        ]
        for f in features:
            st.markdown(f'<div class="sb-feat"><div class="sb-feat-dot"></div>{f}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="sb-rule"><div class="sb-footer">Powered by Claude · Anthropic</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────
def render_hero():
    st.markdown("""
    <div class="hero">
      <div class="hero-deco">AI</div>
      <div class="hero-tag">
        <span class="hero-tag-dot"></span>
        Career Intelligence · Powered by Claude
      </div>
      <h1 class="hero-h1">
        Your resume,<br>
        <em>optimised to get hired.</em>
      </h1>
      <p class="hero-p">
        Get a precise match score, uncover exactly what's working for you,
        spot your fastest growth opportunities, and walk away with
        an AI-crafted plan to land your target role.
      </p>
      <div class="hero-pills">
        <span class="hero-pill">10 + roles supported</span>
        <span class="hero-pill">ATS keyword analysis</span>
        <span class="hero-pill">Claude AI coaching</span>
        <span class="hero-pill">7-day action plan</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  INPUT SECTION
# ─────────────────────────────────────────────────────────────
def render_inputs(PDF_OK):
    """Returns (resume_text_raw, job_description_raw, role, feedback_note, analyze_clicked)"""

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("""
        <div class="input-section-title">Resume</div>
        """, unsafe_allow_html=True)
        mode = st.radio("mode", ["Paste text", "Upload PDF"], horizontal=True, label_visibility="collapsed")

        resume_text_raw = ""
        if mode == "Upload PDF":
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
            if pdf_file:
                from utils import extract_pdf_text
                txt, err = extract_pdf_text(pdf_file)
                if err:
                    st.error(f"PDF error: {err}")
                else:
                    resume_text_raw = txt
                    st.success(f"Extracted {len(txt.split())} words from your resume.")
        else:
            resume_text_raw = st.text_area(
                "resume",
                height=310,
                placeholder="Paste your full resume here…\n\nThe more detail you include, the smarter and more personalised your analysis will be.",
                label_visibility="collapsed",
            )

    with col_r:
        st.markdown("""
        <div class="input-section-title">Job Description</div>
        """, unsafe_allow_html=True)
        job_description_raw = st.text_area(
            "jd",
            height=348,
            placeholder="Paste the full job description here…\n\nEvery sentence helps calibrate your match score and surface the right keywords.",
            label_visibility="collapsed",
        )

    c3, c4 = st.columns([1, 1], gap="large")
    with c3:
        role = st.selectbox("Target Role", [
            "Software Engineer", "Data Analyst", "Data Scientist",
            "Product Manager", "ML Engineer", "DevOps Engineer",
            "Frontend Developer", "Backend Developer", "UX Designer",
            "Cybersecurity Analyst",
        ])
    with c4:
        st.markdown("""
        <div class="input-section-title">
          Recruiter Feedback
          <span style="color:#1a1f38;font-family:'Inter',sans-serif;font-size:0.78rem;font-weight:300;letter-spacing:0;text-transform:none;margin-left:6px;">(optional)</span>
        </div>
        """, unsafe_allow_html=True)
        feedback_note = st.text_area(
            "feedback",
            height=96,
            placeholder="Got a recruiter note? Paste it here for targeted guidance…",
            label_visibility="collapsed",
        )

    analyze_clicked = st.button("✦  Analyse My Profile & Unlock My Roadmap", use_container_width=True)
    return resume_text_raw, job_description_raw, role, feedback_note, analyze_clicked


# ─────────────────────────────────────────────────────────────
#  SCORE + METRICS BAND
# ─────────────────────────────────────────────────────────────
def render_score_band(score, matched_skills, missing_skills, readiness_label, score_color_class, prog_gradient_css):
    skill_pct = int(len(matched_skills) / max(len(matched_skills) + len(missing_skills), 1) * 100)

    # Results header
    st.markdown(f"""
    <div class="results-header">
      <div>
        <div class="results-eyebrow">Analysis complete</div>
        <div class="results-title">Your results are in.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Score band (score left, 4 tiles right)
    st.markdown(f"""
    <div class="score-band">
      <div class="score-main">
        <div class="score-value {score_color_class}">{score}%</div>
        <div class="score-pct">Match Score</div>
        <div class="score-label">{readiness_label}</div>
      </div>
      <div class="metrics-side">
        <div class="metric-tile mt-green">
          <div>
            <div class="metric-tile-val col-g">{len(matched_skills)}</div>
            <div class="metric-tile-lbl">Skills Matched</div>
          </div>
          <div class="metric-tile-sub col-g">{skill_pct}% role coverage</div>
        </div>
        <div class="metric-tile mt-amber">
          <div>
            <div class="metric-tile-val col-a">{len(missing_skills)}</div>
            <div class="metric-tile-lbl">Skills to Add</div>
          </div>
          <div class="metric-tile-sub col-a">Quick wins available</div>
        </div>
        <div class="metric-tile mt-violet" style="grid-column:span 2;">
          <div>
            <div class="metric-tile-val col-v" style="font-size:1.1rem;margin-top:2px;">{readiness_label}</div>
            <div class="metric-tile-lbl" style="margin-top:6px;">Hiring Readiness Level</div>
          </div>
          <div class="metric-tile-sub col-v">See your personalised plan below</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-meta"><span>Profile — JD Alignment</span><span>{score}%</span></div>
      <div class="prog-track">
        <div class="prog-fill" style="width:{score}%;background:{prog_gradient_css};"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_banner(banner_class, banner_icon, readiness_label, readiness_msg):
    st.markdown(f"""
    <div class="status-banner {banner_class}">
      <span class="sb-icon">{banner_icon}</span>
      <span><strong>{readiness_label}:</strong> {readiness_msg}</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  TAB 1 — AI COACHING
# ─────────────────────────────────────────────────────────────
def render_tab_ai(ai_data, ai_err):
    if ai_err:
        st.warning(f"AI coaching unavailable: {ai_err}")
        st.info("Set `ANTHROPIC_API_KEY` in your environment variables to unlock personalised AI feedback.")
        return

    if not ai_data:
        return

    def ai_panel(label, body_html):
        st.markdown(f"""
        <div class="ai-panel">
          <div class="ai-panel-label"><span class="ai-label-pip"></span>{label}</div>
          <div class="ai-panel-body">{body_html}</div>
        </div>
        """, unsafe_allow_html=True)

    ai_panel("Your Candidate Profile", ai_data.get("executive_summary", ""))

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        ai_panel("What Makes You Stand Out", ai_data.get("biggest_strength", ""))
    with c2:
        ai_panel("Your Biggest Growth Opportunity", ai_data.get("growth_opportunity", ""))

    ai_panel("Boost Your ATS Visibility", ai_data.get("ats_verdict", ""))

    bul = ai_data.get("top_bullet_rewrite", {})
    if bul:
        st.markdown(f"""
        <div class="ai-panel">
          <div class="ai-panel-label"><span class="ai-label-pip"></span>Transform Your Resume Bullets</div>
          <div class="bul-compare">
            <div class="bul-box bul-before">
              <div class="bul-tag" style="color:#fca5a5;">Before — weaker version</div>
              {bul.get('original_hint','')}
            </div>
            <div class="bul-box bul-after">
              <div class="bul-tag" style="color:#6ee7b7;">After — high-impact version</div>
              {bul.get('rewritten','')}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    pitch = ai_data.get("one_liner_pitch", "")
    if pitch:
        st.markdown(f"""
        <div class="pitch-spot">
          <div class="pitch-label">Open Every Interview With This</div>
          <div class="pitch-text">{pitch}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  TAB 2 — SKILL MAP
# ─────────────────────────────────────────────────────────────
def render_tab_skills(matched_skills, missing_skills, ai_data):
    def chip_block(skills, cls, icon):
        if not skills:
            return '<p style="color:#1e2440;font-size:0.88rem;">None detected yet.</p>'
        return "".join(f'<span class="chip {cls}">{icon} {s}</span>' for s in skills)

    l, r = st.columns(2, gap="medium")
    with l:
        st.markdown('<div class="tab-section-head">Strengths already working for you</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card">
          <div class="glass-card-label">Confirmed skill matches</div>
          <div class="chips-wrap">{chip_block(matched_skills, "chip-green", "✓")}</div>
        </div>
        """, unsafe_allow_html=True)

    with r:
        st.markdown('<div class="tab-section-head">Skills that will unlock more interviews</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card">
          <div class="glass-card-label">High-value additions to showcase</div>
          <div class="chips-wrap">{chip_block(missing_skills, "chip-amber", "+")}</div>
        </div>
        """, unsafe_allow_html=True)

    if ai_data and ai_data.get("interview_prep"):
        st.markdown('<div class="tab-section-head">Topics that will shine in your interviews</div>', unsafe_allow_html=True)
        chips = "".join(f'<span class="chip chip-violet">→ {t}</span>' for t in ai_data["interview_prep"])
        st.markdown(f"""
        <div class="glass-card">
          <div class="glass-card-label">Prioritised by Claude AI</div>
          <div class="chips-wrap">{chips}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  TAB 3 — KEYWORDS
# ─────────────────────────────────────────────────────────────
def render_tab_keywords(missing_kw, matched_kw):
    st.markdown('<div class="tab-section-head">Keywords to weave into your resume</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
      <div class="glass-card-label">High-impact additions — sorted by JD weight</div>
      <div class="chips-wrap">
        {''.join(f'<span class="chip chip-amber">+ {w}</span>' for w in missing_kw[:22]) if missing_kw
         else '<p style="color:#10b981;font-size:0.88rem;">Keyword coverage is excellent!</p>'}
      </div>
      {'<p style="color:#1e2440;font-size:0.78rem;margin-top:0.8rem;">Add these naturally where truthful — this is how you beat ATS filters.</p>' if missing_kw else ''}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tab-section-head">Keywords already in your favour</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
      <div class="glass-card-label">Confirmed matches with the job description</div>
      <div class="chips-wrap">
        {''.join(f'<span class="chip chip-green">✓ {w}</span>' for w in matched_kw[:22]) if matched_kw
         else '<p style="color:#1e2440;font-size:0.88rem;">Add more role-specific language to surface keyword matches.</p>'}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  TAB 4 — ACTION PLAN
# ─────────────────────────────────────────────────────────────
DEFAULT_PLAN = [
    "Rewrite your resume summary to mirror the job title and top 3 responsibilities.",
    "Add the top missing keywords naturally throughout your resume where truthful.",
    "Upgrade 3–5 bullets using: Action Verb + Quantified Metric + Business Impact.",
    "Align every project description to a specific responsibility in the job posting.",
    "Research the company — mission, recent wins, team structure, product challenges.",
    "Practise the top 5 interview topics out loud using the STAR method.",
    "Apply with your upgraded resume plus a tailored cover letter that opens with your pitch.",
]

def render_tab_plan(ai_data, feedback_note):
    plan = (ai_data.get("week_actions", []) if ai_data else []) or DEFAULT_PLAN

    st.markdown('<div class="tab-section-head">Your personalised 7-day roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><div class="glass-card-label">Curated for your profile</div><div class="timeline">', unsafe_allow_html=True)

    for i, action in enumerate(plan[:7]):
        connector = '<div class="tl-line"></div>' if i < 6 else ''
        st.markdown(f"""
        <div class="tl-item">
          <div class="tl-left">
            <div class="tl-day">Day {i+1}</div>
            {connector}
          </div>
          <div class="tl-text">{action}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    if feedback_note and feedback_note.strip():
        st.markdown('<div class="tab-section-head">Turning that feedback into fuel</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ai-panel">
          <div class="ai-panel-label"><span class="ai-label-pip"></span>Recruiter Feedback You Shared</div>
          <div class="ai-panel-body" style="font-style:italic;color:#6b5fa8;">"{feedback_note.strip()}"</div>
        </div>
        <div class="status-banner sb-violet" style="margin-top:0.5rem;">
          <span class="sb-icon">◉</span>
          <span>Cross-reference this with your Skill Map and Keywords tabs. The root cause is almost always one of the gaps listed there — tackle those first and you'll see a real difference.</span>
        </div>
        """, unsafe_allow_html=True)

    # Closer
    st.markdown("""
    <div class="closer">
      <div class="closer-h">You have everything you need.</div>
      <div class="closer-p">
        Every recruiter is looking for someone who shows up prepared and passionate.
        Follow your plan, refine your resume, and go land that role.
      </div>
    </div>
    """, unsafe_allow_html=True)