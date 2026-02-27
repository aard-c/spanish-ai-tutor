# backend/app/routes/chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Correction
from app.schemas import CorrectionRequest, CorrectionResponse
from app.services.llm_service import call_llm

router = APIRouter()


@router.post("/correct", response_model=CorrectionResponse)
async def correct_sentence(
    request: CorrectionRequest,
    db: AsyncSession = Depends(get_db)
):
    # Call Gemini via service layer
    result = call_llm(request.sentence)

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