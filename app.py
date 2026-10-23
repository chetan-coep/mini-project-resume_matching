
import streamlit as st
from resume_matching import analyze_resume

st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="centered",
)

# Dark/light mode
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "analysis_report" not in st.session_state:
    st.session_state.analysis_report = None

st.title("Resume Matcher")
st.caption("Resume vs. Job Description")

st.toggle("Dark mode", key="dark_mode")

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
    unsafe_allow_html=True,
)

# PDF upload section
st.subheader("Upload Documents")

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
    key="resume_upload",
)

jd_file = st.file_uploader(
    "Upload job description (PDF)",
    type=["pdf"],
    key="jd_upload",
)

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if resume_file is None or jd_file is None:
        st.warning("Please upload both your resume and job description PDFs.")
    else:
        try:
            with st.spinner("Analyzing your resume against the job description..."):
                report = analyze_resume(
                    resume_file.getvalue(),
                    jd_file.getvalue(),
                )

            st.session_state.analysis_report = report
            st.success("Resume analysis completed!")

        except Exception as error:
            st.session_state.analysis_report = None
            st.error(f"Analysis failed: {error}")

# Display analysis results
data = st.session_state.analysis_report

if data is None:
    st.info("Upload both PDFs and click Analyze Resume to see your results.")
    st.stop()

# 1. ATS Score
st.subheader("1. ATS Matching Score")

score = data["calculated_ats_score"]
st.progress(max(0, min(100, int(round(score)))))
st.markdown(f"## {score:.2f}%")
st.caption("Estimated resume-to-job match")

with st.expander("How was this score calculated?"):
    st.write(data["score_explanation"])
    st.write("Component scores:")
    st.write(f"Skills match: {data['skills_match_score']}/100")
    st.write(
        "Internship relevance: "
        f"{data['internship_relevance_score']}/100"
    )
    st.write(f"Academic match: {data['academic_match_score']}/100")
    st.write(f"Project relevance: {data['project_relevance_score']}/100")
    st.write(f"Keyword match: {data['keyword_match_score']}/100")

# 2. Matching fields
st.subheader("2. Matching Fields")

with st.container(border=True):
    matched = data.get("matched_keywords", [])

    if matched:
        for item in matched:
            st.markdown(f"✓ {item}")
    else:
        st.write("No matching fields identified.")

# 3. Non-matching fields
st.subheader("3. Non-Matching Fields")

with st.container(border=True):
    missing = data.get("missing_keywords", [])

    if missing:
        for item in missing:
            st.markdown(f"• {item}")
    else:
        st.write("No missing keywords identified.")

# 4. Improvements
st.subheader("4. What to Improve")

with st.container(border=True):
    suggestions = data.get("improvement_suggestions", [])

    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"• {suggestion}")
    else:
        st.write("No improvement suggestions available.")
