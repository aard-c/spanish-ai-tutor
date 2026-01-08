from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.tutor.prompts import PROMPT

router = APIRouter()

class CorrectionRequest(BaseModel):
    sentence: str


class CorrectionResponse(BaseModel):
    is_correct: bool
    original_sentence: str
    corrected_sentence: str
    grammar_topic: str
    explanation: str

def call_llm(prompt: str, sentence: str) -> dict:
    """
    TEMPORARY mock LLM call.
    We will replace this with a real API call next.
    """
    fake_response = {
        "is_correct": False,
        "original_sentence": sentence,
        "corrected_sentence": "Ayer yo fui al cine",
        "grammar_topic": "preterite tense",
        "explanation": "Because 'ayer' refers to the past, Spanish uses the preterite tense."
    }
    return fake_response

@router.post("/correct", response_model=CorrectionResponse)
def correct_sentence(request: CorrectionRequest):
    result = call_llm(PROMPT, request.sentence)

    return CorrectionResponse(
        is_correct=result["is_correct"],
        original_sentence=result["original_sentence"],
        corrected_sentence=result["corrected_sentence"],
        grammar_topic=result["grammar_topic"],
        explanation=result["explanation"],
    )
