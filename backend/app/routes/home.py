from fastapi import APIRouter

from app.schemas.home_schema import HomePredictionInput, HomePredictionOutput
from app.services.prediction_service import predict_home_price


router = APIRouter()


@router.post("/predict", response_model=HomePredictionOutput)
def predict(data: HomePredictionInput) -> HomePredictionOutput:
    return predict_home_price(data)


@router.get("/properties")
def list_properties() -> dict[str, str]:
    return {"message": "Property database endpoint placeholder"}


@router.get("/history")
def prediction_history() -> dict[str, str]:
    return {"message": "Prediction history endpoint placeholder"}
