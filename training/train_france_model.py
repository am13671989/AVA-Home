"""Train a France-only Random Forest from the official 2024 DVF archive."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import zipfile

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, median_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from build_dvf_dataset import _normalize_dvf_chunk

ROOT = Path(__file__).resolve().parents[1]
DVF_ZIP = ROOT / "data" / "raw" / "valeursfoncieres-2024.txt.zip"
MODEL_PATH = ROOT / "backend" / "app" / "ml" / "france_house_price_model.pkl"
METADATA_PATH = ROOT / "backend" / "app" / "ml" / "france_house_price_model_metadata.json"
FEATURES = ["surface", "rooms", "bedrooms", "garden", "location_price_per_m2"]


def load_national_sample(rows_per_chunk: int = 3_000) -> pd.DataFrame:
    """Sample every chunk so department-sorted DVF data remains nationally representative."""
    frames: list[pd.DataFrame] = []
    with zipfile.ZipFile(DVF_ZIP) as archive:
        txt_name = next(name for name in archive.namelist() if name.endswith(".txt"))
        with archive.open(txt_name) as raw:
            stream = io.TextIOWrapper(raw, encoding="utf-8", errors="replace")
            for chunk_number, chunk in enumerate(pd.read_csv(
                stream, sep="|", dtype=str, chunksize=100_000,
                quoting=csv.QUOTE_NONE, low_memory=False,
            )):
                normalized = _normalize_dvf_chunk(chunk)
                if len(normalized) > rows_per_chunk:
                    normalized = normalized.sample(rows_per_chunk, random_state=42 + chunk_number)
                frames.append(normalized)
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def quality_filter(data: pd.DataFrame) -> pd.DataFrame:
    price_per_m2 = data["price"] / data["surface"]
    filtered = data[
        data["surface"].between(15, 500)
        & data["rooms"].between(1, 12)
        & data["price"].between(20_000, 5_000_000)
        & price_per_m2.between(300, 25_000)
    ].copy()
    # DVF splits these cities into arrondissement-specific commune labels.
    for parent in ("Paris", "Lyon", "Marseille"):
        filtered.loc[filtered["city"].str.startswith(parent + " "), "city"] = parent
    return filtered


def location_baselines(data: pd.DataFrame) -> tuple[dict[str, float], float]:
    price_per_m2 = (data["price"] / data["surface"]).clip(300, 25_000)
    mapping = price_per_m2.groupby(data["city"]).median().to_dict()
    return {str(k): round(float(v), 2) for k, v in mapping.items()}, round(float(price_per_m2.median()), 2)


def model_frame(data: pd.DataFrame, city_baselines: dict[str, float], national_baseline: float) -> pd.DataFrame:
    return pd.DataFrame({
        "surface": data["surface"].astype(float),
        "rooms": data["rooms"].astype(int),
        "bedrooms": data["bedrooms"].astype(int),
        "garden": data["garden"].astype(int),
        "location_price_per_m2": data["city"].map(city_baselines).fillna(national_baseline),
    })


def new_forest() -> TransformedTargetRegressor:
    return TransformedTargetRegressor(
        regressor=RandomForestRegressor(
            n_estimators=60, max_depth=16, min_samples_leaf=8,
            max_features=0.9, random_state=42, n_jobs=-1,
        ),
        func=np.log1p,
        inverse_func=np.expm1,
    )


def main() -> None:
    raw = load_national_sample()
    data = quality_filter(raw)
    train, test = train_test_split(data, test_size=0.20, random_state=42)

    train_locations, train_national = location_baselines(train)
    x_train = model_frame(train, train_locations, train_national)
    x_test = model_frame(test, train_locations, train_national)
    evaluation_model = new_forest()
    evaluation_model.fit(x_train, train["price"])
    predictions = evaluation_model.predict(x_test)
    metrics = {
        "mae_eur": round(float(mean_absolute_error(test["price"], predictions)), 2),
        "median_absolute_error_eur": round(float(median_absolute_error(test["price"], predictions)), 2),
        "mape": round(float(mean_absolute_percentage_error(test["price"], predictions)), 4),
        "r2": round(float(r2_score(test["price"], predictions)), 4),
        "test_rows": len(test),
    }

    metadata = {
        "model_type": "RandomForestRegressor (log-target)",
        "market": "France / official DVF 2024 transactions",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(DVF_ZIP),
        "features": FEATURES,
        "input_rows": len(raw),
        "training_rows": len(train),
        "excluded_rows": len(raw) - len(data),
        "covered_cities": len(train_locations),
        "national_price_per_m2": train_national,
        "city_price_per_m2": train_locations,
        "metrics": metrics,
        "limitations": [
            "DVF records completed transaction values, not current asking prices.",
            "DVF does not provide construction condition, balcony, garage, or build year.",
            "Predictions are experimental and are not professional valuations.",
        ],
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(evaluation_model, MODEL_PATH, compress=3)
    METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({**metrics, "training_rows": len(train), "covered_cities": len(train_locations)}, indent=2))


if __name__ == "__main__":
    main()
