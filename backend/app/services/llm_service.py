import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

from app.services.prompts import PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


def call_llm(sentence: str) -> dict:
    full_prompt = f"""
    {PROMPT}

    Sentence:
    {sentence}
    """

    response = model.generate_content(full_prompt)

    text = response.text

    # Clean markdown formatting if present
    json_text = re.sub(r"```json|```", "", text).strip()

    return json.loads(json_text)