from pathlib import Path

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


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    x = df.drop(columns=["price", "postal_code"])
    y = df["price"]

    numeric_features = ["surface", "rooms", "bedrooms", "garage", "balcony", "garden", "year"]
    categorical_features = ["city", "condition"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
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

    print(f"MAE: {mae:.2f}")
    print(f"R2: {r2:.3f}")
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
