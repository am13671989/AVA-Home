from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "houses.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "houses_clean.csv"


def main() -> None:
    df = pd.read_csv(RAW_PATH)
    df = df.drop_duplicates()
    df = df.dropna(subset=["surface", "price", "city"])

    for column in ["garage", "balcony", "garden"]:
        df[column] = df[column].fillna(0).astype(int)

    for column in ["rooms", "bedrooms", "year"]:
        df[column] = df[column].fillna(df[column].median())

    df["condition"] = df["condition"].fillna("good").str.lower()
    df["city"] = df["city"].str.strip()

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Clean data saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
