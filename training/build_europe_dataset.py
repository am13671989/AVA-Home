from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from build_dvf_dataset import build_dataset as build_france_dvf_dataset


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_PATH = ROOT / "data" / "processed" / "houses_clean.csv"
CITY_TARGETS_PATH = ROOT / "data" / "reference" / "europe_city_targets.csv"
SOURCE_REGISTRY_PATH = ROOT / "data" / "reference" / "europe_property_sources.csv"


def build_france(year: int, max_rows: int) -> pd.DataFrame:
    data = build_france_dvf_dataset(year=year, max_rows=max_rows, chunksize=100_000)
    data.insert(0, "country", "France")
    data.insert(0, "country_iso2", "FR")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a multi-country Ava Home training CSV from implemented official sources."
    )
    parser.add_argument("--france-year", type=int, default=2024)
    parser.add_argument("--france-rows", type=int, default=50_000)
    args = parser.parse_args()

    sources = pd.read_csv(SOURCE_REGISTRY_PATH)
    implemented = sources[sources["status"] == "implemented"]
    print("Implemented sources:")
    print(implemented[["country", "source_name", "training_value"]].to_string(index=False))

    targets = pd.read_csv(CITY_TARGETS_PATH)
    print(f"European target city list contains {len(targets)} cities.")

    frames = [build_france(year=args.france_year, max_rows=args.france_rows)]
    data = pd.concat(frames, ignore_index=True)

    # Keep backward-compatible model columns until the regressor is upgraded to include country.
    model_columns = [
        "surface",
        "rooms",
        "bedrooms",
        "city",
        "postal_code",
        "garage",
        "balcony",
        "garden",
        "year",
        "condition",
        "price",
    ]
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    data[model_columns].to_csv(PROCESSED_PATH, index=False)

    country_counts_path = ROOT / "data" / "processed" / "country_source_counts.csv"
    data.groupby(["country_iso2", "country"]).size().reset_index(name="rows").to_csv(
        country_counts_path, index=False
    )

    print(f"Saved {len(data):,} training rows to {PROCESSED_PATH}")
    print(f"Saved source counts to {country_counts_path}")


if __name__ == "__main__":
    main()
