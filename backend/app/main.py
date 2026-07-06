from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, home


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


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Ava Home API is running"}
