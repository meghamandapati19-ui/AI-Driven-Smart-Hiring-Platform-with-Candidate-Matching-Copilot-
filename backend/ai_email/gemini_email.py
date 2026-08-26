import os
from google import genai
import time

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_email(candidate, job, email_type):

    prompt = f"""
You are an HR Manager.

Candidate Name:
{candidate.get("name","")}

Candidate Skills:
{candidate.get("skills","")}

Experience:
{candidate.get("experience","")}

Job Title:
{job.get("job_title","")}

Company:
{job.get("company_name","")}

Generate a professional {email_type} email.

Rules:
- Professional tone
- Mention candidate name
- Mention job title
- Mention company
- Subject line
- Greeting
- Email body
- Closing

Return only the email.
"""

    
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print("=" * 50)
            print("Attempt:", i + 1)
            print("Gemini Error:", e)
            print("=" * 50)
            time.sleep(5)
    return "Gemini server is busy. Please try again."