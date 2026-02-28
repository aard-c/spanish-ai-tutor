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
    try:   
        response = model.generate_content(full_prompt)
        text = response.text
        json_text = re.sub(r"```json|```", "", text).strip()
        return json.loads(json_text)\
    
    except Exception as e:
        print("Gemini Error: ", e)
        
        return {
            "is correct": False,
            "original_sentence": sentence,
            "corrected_sentence": sentence,
            "grammar_topic": "present tense",
            "explanation": "AI service temporarily unavailable"  
            
        }
        
        
    