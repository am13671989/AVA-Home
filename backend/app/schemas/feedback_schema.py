from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackInput(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    language: str = Field(default="en", max_length=20)
    app_version: str | None = Field(default=None, max_length=30)
    platform: str = Field(default="android", max_length=30)
    current_screen: str | None = Field(default=None, max_length=50)


class FeedbackOutput(BaseModel):
    id: int
    status: str = "saved"
    created_at: datetime
