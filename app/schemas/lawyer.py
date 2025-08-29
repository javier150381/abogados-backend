from typing import List, Optional
from pydantic import BaseModel, EmailStr

class LawyerBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bar_number: Optional[str] = None
    firm: Optional[str] = None
    specialties: List[str]
    languages: Optional[List[str]] = None
    country: Optional[str] = "Ecuador"
    state: Optional[str] = None
    city: Optional[str] = None
    years_experience: Optional[int] = 0
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    rating: Optional[float] = None

class LawyerCreate(LawyerBase):
    pass

class LawyerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bar_number: Optional[str] = None
    firm: Optional[str] = None
    specialties: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    years_experience: Optional[int] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    rating: Optional[float] = None

class LawyerOut(LawyerBase):
    id: int
    class Config:
        from_attributes = True
