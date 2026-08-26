import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = client.models.generate_content(
        model="models/gemini-2.0-flash-lite",
        contents="Write one sentence about Python."
    )

    print(response.text)

except Exception as e:
    print("ERROR:")
    print(e)