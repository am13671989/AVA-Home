from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Feedback
from app.schemas.feedback_schema import FeedbackInput, FeedbackOutput


router = APIRouter()


@router.post("/feedback", response_model=FeedbackOutput, status_code=status.HTTP_201_CREATED)
def save_feedback(data: FeedbackInput, database: Session = Depends(get_db)) -> FeedbackOutput:
    record = Feedback(
        message=data.message.strip(),
        language=data.language,
        app_version=data.app_version,
        platform=data.platform,
        current_screen=data.current_screen,
    )
    database.add(record)
    database.commit()
    database.refresh(record)
    return FeedbackOutput(id=record.id, created_at=record.created_at)
