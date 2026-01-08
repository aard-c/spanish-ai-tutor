from pydantic import BaseModel

class CorrectionRequest(BaseModel):
    sentence: str

class CorrectionResponse(BaseModel):
    is_correct: bool
    original_sentence: str
    corrected_sentence: str
    grammar_topic: str
    explanation: str
