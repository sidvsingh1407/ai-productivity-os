from typing import Optional
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language question or system context")
    k: int = Field(5, ge=1, le=20, description="Number of results to return")

class SearchResponseItem(BaseModel):
    chunk_text: str
    article_number: Optional[str] = None
    section_title: Optional[str] = None
    relevance_score: float = Field(..., description="1 - cosine_distance, higher is better")
