# backend/app/routes/chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Correction
from app.schemas import CorrectionRequest, CorrectionResponse
from app.services.llm_service import call_llm

router = APIRouter()

ALLOWED_TOPICS = {
    "present tense",
    "preterite tense",
    "imperfect tense",
    "ser vs estar",
    "gender agreement",
    "pluralization",
    "articles",
    "prepositions",
    "pronouns",
    "word order",   
}

@router.post("/correct", response_model=CorrectionResponse)
async def correct_sentence(
    request: CorrectionRequest,
    db: AsyncSession = Depends(get_db)
):
    # Call Gemini via service layer
    result = call_llm(request.sentence)
    
    # Set grammar topic to one if it got confused
    if result["grammar_topic"] not in ALLOWED_TOPICS:
        result["grammar_topic"] = "present tense"
        
    # Save to database
    correction = Correction(
        original_sentence=result["original_sentence"],
        corrected_sentence=result["corrected_sentence"],
        grammar_topic=result["grammar_topic"],
        explanation=result["explanation"],
    )

    db.add(correction)
    await db.commit()

    return CorrectionResponse(**result)