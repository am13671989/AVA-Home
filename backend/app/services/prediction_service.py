from pathlib import Path

import joblib
import pandas as pd

from app.schemas.home_schema import HomePredictionInput, HomePredictionOutput


MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "house_price_model.pkl"


def _load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def _fallback_prediction(data: HomePredictionInput) -> float:
    city_factor = {
        "paris": 9500,
        "lyon": 4200,
        "marseille": 3400,
        "grenoble": 3600,
        "toulouse": 3800,
    }.get(data.city.strip().lower(), 3200)
    feature_bonus = (data.garage * 12000) + (data.balcony * 8000) + (data.garden * 18000)
    condition_factor = {"new": 1.12, "good": 1.0, "average": 0.92, "renovation": 0.82}.get(
        data.condition.lower(),
        1.0,
    )
    age_penalty = max(0, 2026 - data.year) * 350
    return max(0, (data.surface * city_factor + feature_bonus - age_penalty) * condition_factor)


def predict_home_price(data: HomePredictionInput) -> HomePredictionOutput:
    model = _load_model()
    input_df = pd.DataFrame(
        [
            {
                "surface": data.surface,
                "rooms": data.rooms,
                "bedrooms": data.bedrooms,
                "city": data.city,
                "garage": data.garage,
                "balcony": data.balcony,
                "garden": data.garden,
                "year": data.year,
                "condition": data.condition,
            }
        ]
    )

    if model is None:
        predicted_price = _fallback_prediction(data)
        confidence_score = 0.45
        message = "Prediction completed with fallback estimator. Train the ML model for better accuracy."
    else:
        predicted_price = float(model.predict(input_df)[0])
        confidence_score = 0.72
        message = "Prediction completed successfully"

    return HomePredictionOutput(
        predicted_price=round(predicted_price, 2),
        confidence_score=confidence_score,
        message=message,
    )
