
import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="centered"
)

# Simple dark/light mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

st.title("Resume Matcher")
st.caption("Resume vs. Job Description")

st.toggle(
    "Dark mode",
    key="dark_mode"
)

if st.session_state.dark_mode:
    background = "#111827"
    foreground = "#F9FAFB"
    card = "#1F2937"
    muted = "#D1D5DB"
else:
    background = "#F8FAFC"
    foreground = "#111827"
    card = "#FFFFFF"
    muted = "#4B5563"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background};
        color: {foreground};
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {card};
        border-radius: 12px;
    }}
    h1, h2, h3, p, li, label {{
        color: {foreground};
    }}
    .muted {{
        color: {muted};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load the saved analysis
report_path = Path("ats_analysis.json")

if not report_path.exists():
    st.warning(
        "No analysis found. Run resume_matching.py first "
        "to generate ats_analysis.json."
    )
    st.stop()

with report_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

# 1. ATS Score
st.subheader("1. ATS Matching Score")

score = data.get("calculated_ats_score", 0)

st.progress(max(0, min(100, int(round(score)))))
st.markdown(f"## {score:.2f}%")
st.caption("Estimated resume-to-job match")

# 2. Matching fields
st.subheader("2. Matching Fields")

matched = data.get("matched_keywords", [])

with st.container(border=True):
    if matched:
        for item in matched:
            st.markdown(f"✓ {item}")
    else:
        st.write("No matching fields identified.")

# 3. Non-matching fields
st.subheader("3. Non-Matching Fields")

missing = data.get("missing_keywords", [])

with st.container(border=True):
    if missing:
        for item in missing:
            st.markdown(f"• {item}")
    else:
        st.write("No missing keywords identified.")

# 4. Improvements
st.subheader("4. What to Improve")

suggestions = data.get("improvement_suggestions", [])

with st.container(border=True):
    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"• {suggestion}")
    else:
        st.write("No improvement suggestions available.")
