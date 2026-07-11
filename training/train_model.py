from pathlib import Path
from datetime import datetime, timezone
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "houses_clean.csv"
MODEL_PATH = ROOT / "backend" / "app" / "ml" / "house_price_model.pkl"
METADATA_PATH = ROOT / "backend" / "app" / "ml" / "house_price_model_metadata.json"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    drop_columns = [column for column in ["price", "postal_code"] if column in df.columns]
    x = df.drop(columns=drop_columns)
    y = df["price"]

    numeric_features = [
        column
        for column in ["surface", "rooms", "bedrooms", "garage", "balcony", "garden", "year"]
        if column in x.columns
    ]
    categorical_features = [
        column
        for column in ["country_iso2", "country", "city", "condition", "data_source"]
        if column in x.columns
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=80,
                    max_depth=18,
                    min_samples_leaf=3,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    metadata = {
        "model_type": "RandomForestRegressor",
        "n_estimators": 80,
        "max_depth": 18,
        "min_samples_leaf": 3,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "training_rows": int(len(df)),
        "features": list(x.columns),
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "target": "price",
        "mae": round(float(mae), 2),
        "r2": round(float(r2), 3),
        "data_file": str(DATA_PATH),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"MAE: {mae:.2f}")
    print(f"R2: {r2:.3f}")
    print(f"Model saved to {MODEL_PATH}")
    print(f"Metadata saved to {METADATA_PATH}")


if __name__ == "__main__":
    main()
