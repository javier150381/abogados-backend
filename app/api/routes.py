from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import SessionLocal
from app.models.lawyer import Lawyer
from app.schemas.lawyer import LawyerCreate, LawyerOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/lawyers", response_model=LawyerOut)
def create_lawyer(payload: LawyerCreate, db: Session = Depends(get_db)):
    item = Lawyer(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        bar_number=payload.bar_number,
        firm=payload.firm,
        specialties=",".join(payload.specialties),
        languages=",".join(payload.languages or []),
        country=payload.country,
        state=payload.state,
        city=payload.city,
        years_experience=payload.years_experience,
        bio=payload.bio,
        photo_url=payload.photo_url,
        rating=payload.rating,
    )
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/lawyers", response_model=List[LawyerOut])
def list_lawyers(
    db: Session = Depends(get_db),
    specialty: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    minExp: int = 0,
    q: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    query = db.query(Lawyer)
    if specialty: query = query.filter(Lawyer.specialties.ilike(f"%{specialty}%"))
    if city:      query = query.filter(Lawyer.city.ilike(f"%{city}%"))
    if state:     query = query.filter(Lawyer.state.ilike(f"%{state}%"))
    if minExp:    query = query.filter(Lawyer.years_experience >= minExp)
    if q:
        like = f"%{q}%"
        query = query.filter((Lawyer.full_name.ilike(like)) | (Lawyer.firm.ilike(like)) | (Lawyer.bio.ilike(like)))
    return query.offset(offset).limit(limit).all()
