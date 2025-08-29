
from fastapi import APIRouter, Depends, HTTPException, Header, status


from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import SessionLocal
from app.core.config import JWT_SECRET
from app.models.lawyer import Lawyer

from app.schemas.lawyer import LawyerCreate, LawyerOut, LawyerUpdate, LawyerVerify


from app.schemas.lawyer import LawyerCreate, LawyerOut, LawyerUpdate, LawyerList



router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(authorization: str = Header(None)):
    if authorization != f"Bearer {JWT_SECRET}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/lawyers", response_model=LawyerOut)
def create_lawyer(
    payload: LawyerCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
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
        verification_status=payload.verification_status,
    )
    db.add(item); db.commit(); db.refresh(item)
    return item



@router.get("/lawyers", response_model=List[LawyerOut])

@router.get("/lawyers", response_model=LawyerList)

def list_lawyers(
    db: Session = Depends(get_db),
    specialty: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    firm: Optional[str] = None,
    minExp: int = 0,
    q: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):

    query = db.query(Lawyer).filter(Lawyer.is_active == True)
    if specialty: query = query.filter(Lawyer.specialties.ilike(f"%{specialty}%"))
    if city:      query = query.filter(Lawyer.city.ilike(f"%{city}%"))
    if state:     query = query.filter(Lawyer.state.ilike(f"%{state}%"))
    if firm:      query = query.filter(Lawyer.firm.ilike(f"%{firm}%"))
    if minExp:    query = query.filter(Lawyer.years_experience >= minExp)

    query = db.query(Lawyer)
    if specialty:
        query = query.filter(Lawyer.specialties.ilike(f"%{specialty}%"))
    if city:
        query = query.filter(Lawyer.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Lawyer.state.ilike(f"%{state}%"))
    if firm:
        query = query.filter(Lawyer.firm.ilike(f"%{firm}%"))
    if minExp:
        query = query.filter(Lawyer.years_experience >= minExp)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (Lawyer.full_name.ilike(like))
            | (Lawyer.firm.ilike(like))
            | (Lawyer.bio.ilike(like))
        )
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {"items": items, "total": total, "limit": limit, "offset": offset}

@router.get("/lawyers/{lawyer_id}", response_model=LawyerOut)
def get_lawyer(lawyer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Lawyer).get(lawyer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    return obj

@router.put("/lawyers/{lawyer_id}", response_model=LawyerOut)

def update_lawyer(lawyer_id: int, payload: LawyerUpdate, db: Session = Depends(get_db)):
    obj = db.query(Lawyer).filter(Lawyer.id == lawyer_id, Lawyer.is_active == True).first()

def update_lawyer(
    lawyer_id: int,
    payload: LawyerUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    obj = db.query(Lawyer).get(lawyer_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    data = payload.dict(exclude_unset=True)
    if "specialties" in data and data["specialties"] is not None:
        data["specialties"] = ",".join(data["specialties"])
    if "languages" in data and data["languages"] is not None:
        data["languages"] = ",".join(data["languages"])
    for campo, valor in data.items():
        setattr(obj, campo, valor)
    db.commit(); db.refresh(obj)
    return obj



@router.delete("/lawyers/{lawyer_id}", response_model=LawyerOut)
def delete_lawyer(lawyer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Lawyer).filter(Lawyer.id == lawyer_id, Lawyer.is_active == True).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    obj.is_active = False
    db.commit(); db.refresh(obj)
    return obj


@router.put("/admin/lawyers/{lawyer_id}/verify", response_model=LawyerOut)
def verify_lawyer(lawyer_id: int, payload: LawyerVerify, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    obj = db.query(Lawyer).get(lawyer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    obj.verification_status = payload.verification_status
    db.commit(); db.refresh(obj)
    return obj

