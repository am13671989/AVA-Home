"""Train the Spain estimator from experimental Barcelona listings."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, median_absolute_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "barcelona_listings_clean.csv"
MODEL_PATH = ROOT / "backend" / "app" / "ml" / "spain_house_price_model.pkl"
METADATA_PATH = ROOT / "backend" / "app" / "ml" / "spain_house_price_model_metadata.json"
FEATURES = ["surface", "bedrooms", "garage", "balcony", "garden", "year", "renovation"]


def prepare_data(source: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, dict]:
    data = source.copy()
    initial_rows = len(data)
    price_per_m2 = data["price"] / data["sq_m_built"]
    valid = (
        data["sq_m_built"].between(20, 500)
        & data["price"].between(25_000, 10_000_000)
        & price_per_m2.between(700, 15_000)
        & data["year_built"].between(1800, 2026)
    )
    data = data.loc[valid].copy()
    frame = pd.DataFrame({
        "surface": data["sq_m_built"].astype(float),
        "bedrooms": data["n_bedrooms"].astype(int),
        "garage": data["parking"].astype(int),
        "balcony": (data["balcony"] | data["terrace"]).astype(int),
        "garden": data["garden"].astype(int),
        "year": data["year_built"].astype(int),
        "renovation": data["needs_renovating"].astype(int),
    })
    quality = {
        "input_rows": initial_rows,
        "training_rows": len(data),
        "excluded_rows": initial_rows - len(data),
        "price_per_m2_filter_eur": [700, 15_000],
        "surface_filter_m2": [20, 500],
    }
    return frame, data["price"].astype(float), quality


def main() -> None:
    x, y, quality = prepare_data(pd.read_csv(DATA_PATH))
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)
    model = TransformedTargetRegressor(
        regressor=RandomForestRegressor(
            n_estimators=350, max_depth=22, min_samples_leaf=2,
            max_features=0.85, random_state=42, n_jobs=-1,
        ),
        func=np.log1p,
        inverse_func=np.expm1,
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics = {
        "mae_eur": round(float(mean_absolute_error(y_test, predictions)), 2),
        "median_absolute_error_eur": round(float(median_absolute_error(y_test, predictions)), 2),
        "mape": round(float(mean_absolute_percentage_error(y_test, predictions)), 4),
        "r2": round(float(r2_score(y_test, predictions)), 4),
        "test_rows": len(x_test),
    }
    metadata = {
        "model_type": "RandomForestRegressor (log-target)",
        "market": "Spain experimental / trained on Barcelona listings",
        "source_file": str(DATA_PATH),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "features": FEATURES,
        "feature_mapping": {
            "surface": "sq_m_built", "bedrooms": "n_bedrooms", "garage": "parking",
            "balcony": "balcony OR terrace", "garden": "garden",
            "year": "year_built", "renovation": "needs_renovating",
        },
        "quality_filters": quality,
        "metrics": metrics,
        "limitations": [
            "Source records are Barcelona asking prices, not completed transactions.",
            "The model is applied to all Spanish cities without a city adjustment.",
            "Predictions are experimental and are not professional valuations.",
        ],
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps({"model": str(MODEL_PATH), **metrics, **quality}, indent=2))


if __name__ == "__main__":
    main()
