from pathlib import Path
import json
from functools import lru_cache

import joblib
import pandas as pd

from app.schemas.home_schema import HomePredictionInput, HomePredictionOutput


SPAIN_MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "spain_house_price_model.pkl"
SPAIN_METADATA_PATH = Path(__file__).resolve().parents[1] / "ml" / "spain_house_price_model_metadata.json"
FRANCE_MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "france_house_price_model.pkl"
FRANCE_METADATA_PATH = Path(__file__).resolve().parents[1] / "ml" / "france_house_price_model_metadata.json"
SPANISH_CITIES = {"barcelona", "madrid", "seville", "sevilla", "valencia"}
FRENCH_CITIES = {"paris", "lyon", "marseille", "toulouse", "nice", "bordeaux", "lille", "nantes", "montpellier", "rennes"}


def _is_spain(data: HomePredictionInput) -> bool:
    country_iso2 = (data.country_iso2 or "").strip().upper()
    country = (data.country or "").strip().lower()
    if country_iso2 or country:
        return country_iso2 == "ES" or country in {"spain", "españa", "espana"}
    return data.city.strip().lower() in SPANISH_CITIES


def _is_france(data: HomePredictionInput) -> bool:
    country_iso2 = (data.country_iso2 or "").strip().upper()
    country = (data.country or "").strip().lower()
    if country_iso2 or country:
        return country_iso2 == "FR" or country in {"france", "fr"}
    return data.city.strip().lower() in FRENCH_CITIES


def _spain_input_frame(data: HomePredictionInput) -> pd.DataFrame:
    return pd.DataFrame([{
        "surface": data.surface,
        "bedrooms": data.bedrooms,
        "garage": data.garage,
        "balcony": data.balcony,
        "garden": data.garden,
        "year": data.year,
        "renovation": int(data.condition.strip().lower() == "renovation"),
    }])


@lru_cache(maxsize=1)
def _load_spain_model():
    return joblib.load(SPAIN_MODEL_PATH)


@lru_cache(maxsize=1)
def _load_spain_metadata() -> dict:
    return json.loads(SPAIN_METADATA_PATH.read_text(encoding="utf-8")) if SPAIN_METADATA_PATH.exists() else {}


def _predict_spain(data: HomePredictionInput) -> HomePredictionOutput | None:
    if not _is_spain(data) or not SPAIN_MODEL_PATH.exists():
        return None
    model = _load_spain_model()
    metadata = _load_spain_metadata()
    predicted_price = max(0.0, float(model.predict(_spain_input_frame(data))[0]))
    metrics = metadata.get("metrics", {})
    mape = float(metrics.get("mape", 0.33))
    confidence_score = min(0.82, max(0.50, 1 - mape))
    range_factor = min(0.40, max(0.20, mape))
    price_per_m2 = predicted_price / data.surface if data.surface else None
    return HomePredictionOutput(
        predicted_price=round(predicted_price, 2),
        confidence_score=round(confidence_score, 3),
        message="Experimental Spain estimate trained on real Barcelona listing data",
        model_type=metadata.get("model_type", "RandomForestRegressor"),
        data_scope=f"{metadata.get('quality_filters', {}).get('training_rows', 'unknown')} filtered Barcelona listings; applied Spain-wide",
        estimated_price_per_m2=round(price_per_m2, 2) if price_per_m2 else None,
        price_range_low=round(predicted_price * (1 - range_factor), 2),
        price_range_high=round(predicted_price * (1 + range_factor), 2),
    )


@lru_cache(maxsize=1)
def _load_france_model():
    return joblib.load(FRANCE_MODEL_PATH)


@lru_cache(maxsize=1)
def _load_france_metadata() -> dict:
    return json.loads(FRANCE_METADATA_PATH.read_text(encoding="utf-8"))


def _predict_france(data: HomePredictionInput) -> HomePredictionOutput:
    if not FRANCE_MODEL_PATH.exists():
        raise ValueError("The France model has not been trained yet")
    metadata = _load_france_metadata()
    city_baselines = metadata.get("city_price_per_m2", {})
    location_price = float(city_baselines.get(data.city.strip().title(), metadata["national_price_per_m2"]))
    input_frame = pd.DataFrame([{
        "surface": data.surface,
        "rooms": data.rooms,
        "bedrooms": data.bedrooms,
        "garden": data.garden,
        "location_price_per_m2": location_price,
    }])
    predicted_price = max(0.0, float(_load_france_model().predict(input_frame)[0]))
    metrics = metadata.get("metrics", {})
    mape = float(metrics.get("mape", 0.49))
    confidence_score = min(0.75, max(0.45, 1 - mape))
    range_factor = min(0.50, max(0.25, mape))
    price_per_m2 = predicted_price / data.surface if data.surface else None
    return HomePredictionOutput(
        predicted_price=round(predicted_price, 2),
        confidence_score=round(confidence_score, 3),
        message="Experimental France estimate trained on official DVF 2024 transactions",
        model_type=metadata.get("model_type", "RandomForestRegressor"),
        data_scope=f"{metadata.get('training_rows', 'unknown')} France DVF transactions",
        estimated_price_per_m2=round(price_per_m2, 2) if price_per_m2 else None,
        price_range_low=round(predicted_price * (1 - range_factor), 2),
        price_range_high=round(predicted_price * (1 + range_factor), 2),
    )


def predict_home_price(data: HomePredictionInput) -> HomePredictionOutput:
    spain_prediction = _predict_spain(data)
    if spain_prediction is not None:
        return spain_prediction
    if _is_france(data):
        return _predict_france(data)
    raise ValueError("Unsupported country. Ava Home currently supports only France and Spain.")
