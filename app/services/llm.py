from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def get_ai_response(message: str, context: str) -> str:

    prompt = f"""
You are an AI assistant that answers questions about insurance policies.

Your task is to answer the user's question using ONLY the information
provided in the retrieved policy context.

Rules:
1. Do not use outside knowledge.
2. Do not assume or invent policy coverage, eligibility, exclusions,
   waiting periods, claim conditions, premiums, or benefits.
3. If the answer is not clearly available in the provided context, say:
   "I couldn't find that information in the uploaded policy documents."
4. Give a clear and concise answer.
5. If the context contains relevant conditions or exceptions, mention them.
6. If source information such as policy name or page number is available
   in the context, mention it when useful.
7. If the question asks whether something is covered, distinguish between
   "covered", "not covered", and "not specified in the provided documents".
8. Do not provide legal or financial advice. Base the response strictly
   on the uploaded policy documents.

Retrieved Policy Context:
{context}

User Question:
{message}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text