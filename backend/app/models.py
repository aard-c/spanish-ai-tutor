from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from datetime import datetime

class Correction(Base):
    __tablename__ = "corrections"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_sentence: Mapped[str] = mapped_column(Text)
    corrected_sentence: Mapped[str] = mapped_column(Text)
    grammar_topic: Mapped[str] = mapped_column(String(100))
    explanation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
)
