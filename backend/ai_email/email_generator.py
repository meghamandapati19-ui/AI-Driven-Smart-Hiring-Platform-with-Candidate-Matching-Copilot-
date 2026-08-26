from services.groq_service import generate_response


def create_email(candidate, job, email_type):

    prompt = f"""

You are an expert HR recruiter.

Generate a professional {email_type} email.

Candidate Details:
Name: {candidate['name']}
Email: {candidate['email']}
Skills: {candidate['skills']}

Job Details:
Job Title: {job['job_title']}
Company: {job['company_name']}

Create:

1. Email Subject
2. Professional greeting
3. Email body
4. Closing message

Keep the email polite and professional.

"""

    email = generate_response(prompt)

    return {
        "email": email
    }