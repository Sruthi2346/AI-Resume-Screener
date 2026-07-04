import os
from groq import Groq
from dotenv import load_dotenv
from app.prompts import EXTRACT_CANDIDATE_DETAILS

# 🔐 Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# 🤖 Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def extract_resume_data(resume_data):

    try:
        # 🧠 Create prompt
        prompt = EXTRACT_CANDIDATE_DETAILS.format(
            resume_text=resume_data
        )

        # 🚀 Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ working model
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0  # 🔥 stable output
        )

        # ✅ Extract response text
        result = response.choices[0].message.content

        print("\n🔹 GROQ RESPONSE:\n", result)

        # ✅ Return plain text (NO JSON parsing)
        return result

    except Exception as e:
        print("❌ ERROR:", str(e))

        return f"""
Candidate Details:
Name: Unknown
Email: Unknown
Phone: Unknown
Skills:

Match Score: 0

Final Decision: Rejected

Reason:
Error occurred while processing: {str(e)}
"""