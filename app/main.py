from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine
from app.models.base import Base

from app.api.v1.endpoints import auth as auth_endpoint
from app.api.v1.endpoints import expenses as expenses_endpoint


def create_app() -> FastAPI:
    app = FastAPI(title="Expense Tracker API", version="1.0.0")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth_endpoint.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(expenses_endpoint.router, prefix="/api/v1/expenses", tags=["expenses"])

    # Static frontend
    app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)


