from fastapi.testclient import TestClient

from app.database.connection import SessionLocal
from app.database.models import Feedback
from app.main import app


client = TestClient(app)


def test_feedback_is_persisted():
    response = client.post(
        "/api/feedback",
        json={
            "message": "The estimate screen was useful.",
            "language": "en",
            "app_version": "0.1-test",
            "platform": "android",
            "current_screen": "Result",
        },
    )
    assert response.status_code == 201
    feedback_id = response.json()["id"]

    database = SessionLocal()
    try:
        saved = database.get(Feedback, feedback_id)
        assert saved is not None
        assert saved.message == "The estimate screen was useful."
        assert saved.current_screen == "Result"
        database.delete(saved)
        database.commit()
    finally:
        database.close()


def test_blank_feedback_is_rejected():
    response = client.post("/api/feedback", json={"message": ""})
    assert response.status_code == 422
