# Resume Matcher

Resume Matcher is a Python application that compares a resume with a job description and provides an estimated ATS match score.

## Features

- Upload a resume and job description in PDF format.
- Calculate an estimated ATS matching score.
- Identify matching keywords.
- Find missing keywords.
- Get suggestions to improve your resume.
- Switch between dark and light modes.

## Technologies Used

- Python
- Streamlit
- Groq API
- Pydantic
- pypdf

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/mini-project-resume_matching.git
   cd mini-project-resume_matching
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Create a `.env` file in the project directory and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

4. Run the application:

   ```bash
   uv run streamlit run app.py
   ```

5. Open the local URL shown in your terminal.

## How to Use

1. Upload your resume as a PDF.
2. Upload the job description as a PDF.
3. Click **Analyze Resume**.
4. View your matching score, matching keywords, missing keywords, and improvement suggestions.

## ATS Score Calculation

The score is calculated using these criteria:

- Skills match: 30%
- Internship and experience relevance: 20%
- Academic match: 10%
- Project relevance: 20%
- Job-description keyword match: 20%

The score is an estimate and does not guarantee selection or represent the score used by any specific company's ATS.

## Privacy

Your resume and job description are sent to the Groq API for analysis. Do not upload sensitive documents unless you are comfortable with this processing.

Keep your API key and personal documents out of the public GitHub repository.

## Author

Chetan Kamble
