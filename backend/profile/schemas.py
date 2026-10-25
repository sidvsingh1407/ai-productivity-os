from typing import List, Optional
from pydantic import BaseModel


class ProfileFact(BaseModel):
    category: str
    value: str
    source_text: Optional[str] = None
    is_verified: bool = False


class ProfileEntry(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    facts: List[ProfileFact] = []


class ProfileDraftResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    links: List[str] = []
    experience: List[ProfileEntry] = []
    education: List[ProfileEntry] = []
    projects: List[ProfileEntry] = []
    certifications: List[str] = []
    skills: List[str] = []
    positions_of_responsibility: List[ProfileEntry] = []
    volunteering: List[ProfileEntry] = []
    awards: List[str] = []
