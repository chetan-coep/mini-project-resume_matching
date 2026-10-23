# import the libraries 
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ConfigDict
from pypdf import PdfReader

# load the environment variables from the .env file
load_dotenv()
# get the API key from the environment variable
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# create a Groq client using the API key
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b" # as llama-2-70b is not available in the free tier, we will use gpt-oss-120b instead

# read the resume PDF file
resume_path = Path("resume.pdf")
reader = PdfReader(resume_path)
resume_text = "\n".join(
    page.extract_text() or ""
    for page in reader.pages
)
if not resume_text.strip():
    raise ValueError("Could not extract text from resume PDF.")


# read the jd file 
jd_path = Path("jd.pdf")
readerj = PdfReader(jd_path)
jd_text = "\n".join(
    page.extract_text() or ""
    for page in readerj.pages
)
if not jd_text.strip():
    raise ValueError("Could not extract text from resume PDF.")


# define the Pydantic model for the resume information

class Internship(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str | None
    role: str | None
    duration: str | None
    duration_months: int | None
    description: str
    skills_used: list[str]


class AcademicRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    degree: str | None
    institution: str | None
    graduation_year: int | None
    result_type: str | None
    result_value: str | None
    relevant_coursework: list[str]


class ATSAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_name: str | None
    skills: list[str]
    internships: list[Internship]
    academics: list[AcademicRecord]
    projects: list[str]
    certifications: list[str]

    matched_keywords: list[str]
    missing_keywords: list[str]

    skills_match_score: int
    internship_relevance_score: int
    academic_match_score: int
    project_relevance_score: int
    keyword_match_score: int

    overall_ats_score: int
    score_explanation: str
    improvement_suggestions: list[str]

# system message for the model
message_system={
    "role": "system",
    "content": """
        You are a resume information extraction and ATS analysis assistant.
        First, extract factual information from the resume:
        - Candidate name
        - Technical and professional skills
        - Internships, including company, role, duration, and description
        - Academic qualifications, CGPA, percentage, and relevant coursework
        - Projects and certifications

        Then compare the resume with the supplied job description.

        ATS scoring criteria:
        - Skills match: 30%
        - Internship and experience relevance: 20%
        - Academic match: 10%
        - Project relevance: 20%
        - Job-description keyword match: 20%

        Calculate the overall ATS score as the weighted average
        of these five component scores.

        Each component score must be an integer from 0 to 100.
        The overall score must also be between 0 and 100.

        Rules:
        - Use evidence from the resume and job description.
        - Do not invent skills, internships, durations, grades, or qualifications.
        - Use empty lists when no items are found.
        - Use null for missing scalar information.
        - Distinguish missing information from a confirmed lack of qualification.
        - Identify keywords that match and keywords that are missing.
        - Explain the score and suggest truthful resume improvements.
        - Do not reward a candidate for claiming a skill that is not supported
        by the resume.
        - Return data matching the provided JSON schema.
    """
}

user_messages ={
    "role": "user",
    "content": f"""
        Analyze this resume against the job description.

        RESUME TEXT:
        {resume_text}

        JOB DESCRIPTION:
        {jd_text}
    """
}


messages = [message_system, user_messages]

# response from the model
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "ats_analysis",
            "strict": True,
            "schema": ATSAnalysis.model_json_schema()
        }
    }
)

# Extract the response
ai_response = response.choices[0].message.content

if not ai_response:
    raise ValueError("The AI returned an empty response.")

# Validate the JSON using Pydantic
customer_issue = ATSAnalysis.model_validate_json(ai_response)

# Calculate the overall ATS score based on the weighted average of the component scores
ats_score = (
    customer_issue.skills_match_score * 0.30
    + customer_issue.internship_relevance_score * 0.20
    + customer_issue.academic_match_score * 0.10
    + customer_issue.project_relevance_score * 0.20
    + customer_issue.keyword_match_score * 0.20
)

ats_score = round(ats_score, 2)

print("\n========== RESUME MATCH REPORT ==========")

print(f"\nATS Matching Percentage: {ats_score}%")

# Matching fields
print("\n✅ MATCHING FIELDS")
if customer_issue.matched_keywords:
    for item in customer_issue.matched_keywords:
        print(f"  + {item}")
else:
    print("  No matching keywords identified.")

# Non-matching fields
print("\n❌ NON-MATCHING FIELDS")
if customer_issue.missing_keywords:
    for item in customer_issue.missing_keywords:
        print(f"  - {item}")
else:
    print("  No missing keywords identified.")

# Improvement suggestions
print("\n========== IMPROVEMENT SUGGESTIONS ==========")
for suggestion in customer_issue.improvement_suggestions:
    print(f"  - {suggestion}")


# conneting it to ui 
import json

report = customer_issue.model_dump()
report["calculated_ats_score"] = ats_score

Path("ats_analysis.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)