from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.tutor.prompts import PROMPT
from app.database import get_db
from app.models import Correction

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
    return {
        "is_correct": False,
        "original_sentence": sentence,
        "corrected_sentence": "Ayer yo fui al cine",
        "grammar_topic": "preterite tense",
        "explanation": "Because 'ayer' refers to the past, Spanish uses the preterite tense."
    }


@router.post("/correct", response_model=CorrectionResponse)
async def correct_sentence(
    request: CorrectionRequest,
    db: AsyncSession = Depends(get_db)
):
    result = call_llm(PROMPT, request.sentence)

    correction = Correction(
        original_sentence=result["original_sentence"],
        corrected_sentence=result["corrected_sentence"],
        grammar_topic=result["grammar_topic"],
        explanation=result["explanation"],
    )

    db.add(correction)
    await db.commit()

    return CorrectionResponse(**result)
