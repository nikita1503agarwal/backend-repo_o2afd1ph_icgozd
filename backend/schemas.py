from pydantic import BaseModel, Field
from typing import List, Optional

# Schemas define collections. Class name lowercased = collection name.

class Emergency(BaseModel):
    mode: str = Field(default="emergency")
    category: str  # accident | harassment | fraud | threat | other
    description: str
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    jurisdiction: Optional[str] = None  # e.g., IN | AE

class Query(BaseModel):
    mode: str = Field(default="law")
    question: str
    depth: str = Field(default="normal", description="normal | deep")
    jurisdiction: Optional[str] = None
    topics: List[str] = []

class Draft(BaseModel):
    mode: str = Field(default="draft")
    doc_type: str  # contract | nda | petition | agreement
    instructions: str
    jurisdiction: Optional[str] = None
    file_url: Optional[str] = None
