from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import router
from app.core.error_handlers import db_error_handler, http_error_handler
from app.db.session import Base, engine

# Crear tablas (SQLite); en Postgres luego usaremos Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Abogados API")

app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(SQLAlchemyError, db_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod limita a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
