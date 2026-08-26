from interview.gemini_questions import generate_gemini_questions

def generate_questions(candidate, job):
    response = generate_gemini_questions(candidate, job)

    return {
        "gemini_response": response
    }