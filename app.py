

import streamlit as st

from styles import CSS
from utils import (
    PDF_OK,
    clean_text,
    calculate_match_tfidf,
    find_keyword_gaps,
    find_role_skill_gaps,
    get_readiness,
    score_color_class,
    prog_gradient,
    banner_cls,
    get_ai_feedback,
)
from components import (
    render_sidebar,
    render_hero,
    render_inputs,
    render_score_band,
    render_banner,
    render_tab_ai,
    render_tab_skills,
    render_tab_keywords,
    render_tab_plan,
)

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HireMe AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  INJECT STYLES
# ─────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
render_sidebar()

# ─────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────
render_hero()

# ─────────────────────────────────────────────────────────────
#  INPUTS
# ─────────────────────────────────────────────────────────────
resume_text_raw, jd_raw, role, feedback_note, analyze_clicked = render_inputs(PDF_OK)

# ─────────────────────────────────────────────────────────────
#  ANALYSIS
# ─────────────────────────────────────────────────────────────
if analyze_clicked:
    if not resume_text_raw or not jd_raw:
        st.warning("Please add both your resume and the job description to get started.")
        st.stop()

    # ── Scoring ──
    with st.spinner("Calculating your match score…"):
        rc = clean_text(resume_text_raw)
        jc = clean_text(jd_raw)
        score          = calculate_match_tfidf(rc, jc)
        missing_kw, matched_kw   = find_keyword_gaps(rc, jc)
        matched_skills, missing_skills = find_role_skill_gaps(rc, role)
        readiness_label, r_color, r_msg = get_readiness(score)
        sc  = score_color_class(score)
        pg  = prog_gradient(score)
        bcls, bicon = banner_cls(r_color)

    # ── AI coaching ──
    with st.spinner("Getting your personalised AI coaching from Claude…"):
        ai_data, ai_err = get_ai_feedback(
            resume_text_raw, jd_raw, role,
            matched_skills, missing_skills, missing_kw, score,
        )

    # ─────────────────────────────────────────────────────
    #  RESULTS
    # ─────────────────────────────────────────────────────
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Score + metrics
    render_score_band(score, matched_skills, missing_skills, readiness_label, sc, pg)

    # Status banner
    render_banner(bcls, bicon, readiness_label, r_msg)

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "✦  AI Coaching",
        "◈  Skill Map",
        "⌖  Keywords",
        "→  7-Day Roadmap",
    ])

    with tab1:
        render_tab_ai(ai_data, ai_err)

    with tab2:
        render_tab_skills(matched_skills, missing_skills, ai_data)

    with tab3:
        render_tab_keywords(missing_kw, matched_kw)

    with tab4:
        render_tab_plan(ai_data, feedback_note)