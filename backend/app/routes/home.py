from fastapi import APIRouter, HTTPException

from app.schemas.home_schema import HomePredictionInput, HomePredictionOutput
from app.services.prediction_service import predict_home_price


router = APIRouter()


@router.post("/predict", response_model=HomePredictionOutput)
def predict(data: HomePredictionInput) -> HomePredictionOutput:
    try:
        return predict_home_price(data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/properties")
def list_properties() -> dict[str, str]:
    return {"message": "Property database endpoint placeholder"}


@router.get("/history")
def prediction_history() -> dict[str, str]:
    return {"message": "Prediction history endpoint placeholder"}
