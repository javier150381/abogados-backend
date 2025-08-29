from typing import List, Optional

from pydantic import BaseModel, conint, constr, validator


# Reusable constrained types
EmailStr = constr(strip_whitespace=True, regex=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
BarNumber = constr(strip_whitespace=True, regex=r"^\d{5,10}$")
YearsExperience = conint(ge=0, le=80)


class LawyerShared(BaseModel):
    """Shared attributes and validators for lawyers."""

    full_name: Optional[constr(strip_whitespace=True)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(strip_whitespace=True)] = None
    bar_number: Optional[BarNumber] = None
    firm: Optional[constr(strip_whitespace=True)] = None
    specialties: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    country: Optional[constr(strip_whitespace=True)] = "Ecuador"
    state: Optional[constr(strip_whitespace=True)] = None
    city: Optional[constr(strip_whitespace=True)] = None
    years_experience: Optional[YearsExperience] = 0
    bio: Optional[constr(strip_whitespace=True)] = None
    photo_url: Optional[constr(strip_whitespace=True)] = None
    rating: Optional[float] = None

    @validator("specialties", "languages", pre=True)
    def normalize_lists(cls, v):  # type: ignore[override]
        if v is None:
            return v
        if isinstance(v, str):
            v = v.split(",")
        return [str(item).strip() for item in v if str(item).strip()]

    @validator(
        "full_name",
        "email",
        "phone",
        "bar_number",
        "firm",
        "country",
        "state",
        "city",
        "bio",
        "photo_url",
        pre=True,
    )
    def strip_strings(cls, v):  # type: ignore[override]
        if isinstance(v, str):
            return v.strip()
        return v


class LawyerBase(LawyerShared):
    full_name: constr(strip_whitespace=True)
    specialties: List[str]


class LawyerCreate(LawyerBase):
    pass


class LawyerUpdate(LawyerShared):
    pass


class LawyerOut(LawyerBase):
    id: int

    class Config:
        from_attributes = True

