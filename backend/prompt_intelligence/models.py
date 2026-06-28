import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class PromptHistory(Base):
    __tablename__ = "prompt_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_prompt: Mapped[str] = mapped_column(String, nullable=False)
    improved_prompt: Mapped[str] = mapped_column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
