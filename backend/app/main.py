from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.models import Base
from app.routes import feedback, health, home


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Ava Home API",
    description="Property price estimation service for the Ava ecosystem.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(home.router, prefix="/api/home", tags=["Ava Home"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Ava Home API is running"}
