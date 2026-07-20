from typing import Optional
from pydantic import BaseModel

class Citation(BaseModel):
    chunk_text: str
    citation: str
    article_number: Optional[str] = None
    section_title: Optional[str] = None
    relevance_score: float
