import os
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_interview_questions(job_description, candidate_resume):
    """
    Generate interview questions based on the job description
    and candidate resume.
    """

    prompt = f"""
You are an AI recruitment assistant.

Generate interview questions for the candidate based on the
job description and resume given below.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{candidate_resume}

Generate:
1. 5 Technical questions
2. 3 HR/Behavioral questions
3. 2 Questions based specifically on the candidate's resume

Keep the questions clear, relevant and suitable for an interview.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating interview questions: {str(e)}"