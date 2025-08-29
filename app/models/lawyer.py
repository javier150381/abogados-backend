from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from app.db.session import Base


class Lawyer(Base):
    __tablename__ = "lawyers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False, index=True)
    email = Column(String(120), index=True)
    phone = Column(String(50))
    bar_number = Column(String(80))
    firm = Column(String(180))
    specialties = Column(Text, nullable=False)   # CSV: "penal,familia"
    languages = Column(Text)                     # CSV: "es,en"
    country = Column(String(100), default="Ecuador")
    state = Column(String(100))
    city = Column(String(100), index=True)
    years_experience = Column(Integer, default=0)
    bio = Column(Text)
    photo_url = Column(String(300))
    rating = Column(Float)
    is_active = Column(Boolean, default=True, nullable=False)

