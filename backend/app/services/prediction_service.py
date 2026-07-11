from pathlib import Path
import json

import joblib
import pandas as pd

from app.schemas.home_schema import HomePredictionInput, HomePredictionOutput


MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "house_price_model.pkl"
METADATA_PATH = Path(__file__).resolve().parents[1] / "ml" / "house_price_model_metadata.json"


def _load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def _load_metadata() -> dict:
    if not METADATA_PATH.exists():
        return {}
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def _fallback_prediction(data: HomePredictionInput) -> tuple[float, str]:
    city_factor = {
        "paris": 9500,
        "lyon": 4200,
        "marseille": 3400,
        "grenoble": 3600,
        "toulouse": 3800,
        "madrid": 4700,
        "barcelona": 5100,
        "milan": 5900,
        "berlin": 5600,
        "london": 9800,
        "amsterdam": 7800,
        "vienna": 6200,
        "lisbon": 5200,
        "zurich": 13500,
    }.get(data.city.strip().lower(), 3200)
    feature_bonus = (data.garage * 12000) + (data.balcony * 8000) + (data.garden * 18000)
    condition_factor = {"new": 1.12, "good": 1.0, "average": 0.92, "renovation": 0.82}.get(
        data.condition.lower(),
        1.0,
    )
    age_penalty = max(0, 2026 - data.year) * 350
    prediction = max(0, (data.surface * city_factor + feature_bonus - age_penalty) * condition_factor)
    return prediction, "European fallback city baseline"


def _input_frame(data: HomePredictionInput, features: list[str] | None = None) -> pd.DataFrame:
    values = {
        "country_iso2": data.country_iso2 or "",
        "country": data.country or "",
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
    if features:
        values = {feature: values.get(feature, "") for feature in features}
    return pd.DataFrame([values])


def predict_home_price(data: HomePredictionInput) -> HomePredictionOutput:
    model = _load_model()
    metadata = _load_metadata()
    input_df = _input_frame(data, metadata.get("features"))

    if model is None:
        predicted_price, scope = _fallback_prediction(data)
        confidence_score = 0.45
        message = "Prediction completed with fallback estimator. Train the ML model for better accuracy."
        model_type = "fallback_city_baseline"
        data_scope = scope
    else:
        predicted_price = float(model.predict(input_df)[0])
        r2 = float(metadata.get("r2", 0))
        confidence_score = min(0.82, max(0.5, 0.62 + (r2 * 0.2)))
        message = "Prediction completed with trained Random Forest model"
        model_type = metadata.get("model_type", "RandomForestRegressor")
        data_scope = f"{metadata.get('training_rows', 'unknown')} training rows"

    price_per_m2 = predicted_price / data.surface if data.surface else None
    range_factor = 0.18 if model is not None else 0.25

    return HomePredictionOutput(
        predicted_price=round(predicted_price, 2),
        confidence_score=confidence_score,
        message=message,
        model_type=model_type,
        data_scope=data_scope,
        estimated_price_per_m2=round(price_per_m2, 2) if price_per_m2 else None,
        price_range_low=round(predicted_price * (1 - range_factor), 2),
        price_range_high=round(predicted_price * (1 + range_factor), 2),
    )
