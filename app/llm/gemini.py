import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

def generate_answer(question, context):

    import time

    prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question ONLY using the supplied context.

Rules:
- Do not invent facts.
- Use the retrieved evidence.
- If the context does not contain enough information, say:
  "The available knowledge base does not contain enough information."
- Give a concise and useful answer.

USER QUESTION:
{question}

RETRIEVED CONTEXT:
{context}
"""

    for attempt in range(3):
        try:
            print(f"\nGemini attempt {attempt + 1}/3")

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            print("Gemini response generated successfully.")

            return response.text

        except ServerError as error:
            print("Gemini temporarily unavailable.")

            if attempt < 2:
                wait_time = 5 * (attempt + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise error