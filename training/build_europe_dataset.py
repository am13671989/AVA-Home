from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from build_dvf_dataset import build_dataset as build_france_dvf_dataset


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_PATH = ROOT / "data" / "processed" / "houses_clean.csv"
CITY_TARGETS_PATH = ROOT / "data" / "reference" / "europe_city_targets.csv"
CITY_BASELINES_PATH = ROOT / "data" / "reference" / "europe_city_price_baselines.csv"
SOURCE_REGISTRY_PATH = ROOT / "data" / "reference" / "europe_property_sources.csv"


def build_france(year: int, max_rows: int) -> pd.DataFrame:
    data = build_france_dvf_dataset(year=year, max_rows=max_rows, chunksize=100_000)
    data.insert(0, "country", "France")
    data.insert(0, "country_iso2", "FR")
    data["data_source"] = "official_transaction"
    return data


def build_city_baselines(rows_per_city: int) -> pd.DataFrame:
    baselines = pd.read_csv(CITY_BASELINES_PATH)
    property_templates = [
        {"surface": 35, "rooms": 1, "bedrooms": 0, "condition": "renovation", "factor": 0.88},
        {"surface": 50, "rooms": 2, "bedrooms": 1, "condition": "good", "factor": 0.96},
        {"surface": 70, "rooms": 3, "bedrooms": 2, "condition": "good", "factor": 1.00},
        {"surface": 90, "rooms": 4, "bedrooms": 3, "condition": "excellent", "factor": 1.08},
        {"surface": 120, "rooms": 5, "bedrooms": 4, "condition": "new", "factor": 1.16},
        {"surface": 160, "rooms": 6, "bedrooms": 4, "condition": "good", "factor": 1.04},
    ]
    rows = []
    for city_index, city in baselines.iterrows():
        city_priority_adjustment = 1 + ((city_index % 5) - 2) * 0.015
        for row_number in range(rows_per_city):
            template = property_templates[row_number % len(property_templates)]
            cycle_adjustment = 1 + ((row_number % 7) - 3) * 0.018
            surface = int(template["surface"] * (1 + ((row_number % 3) - 1) * 0.06))
            price = round(
                surface
                * float(city["price_per_m2_eur"])
                * template["factor"]
                * city_priority_adjustment
                * cycle_adjustment
            )
            rows.append(
                {
                    "country_iso2": city["country_iso2"],
                    "country": city["country"],
                    "surface": surface,
                    "rooms": template["rooms"],
                    "bedrooms": template["bedrooms"],
                    "city": city["city"],
                    "postal_code": "",
                    "garage": 1 if surface >= 90 and row_number % 2 == 0 else 0,
                    "balcony": 1 if template["rooms"] >= 2 and row_number % 3 != 0 else 0,
                    "garden": 1 if surface >= 120 and row_number % 4 == 0 else 0,
                    "year": 2024 - (row_number % 8),
                    "condition": template["condition"],
                    "price": int(price),
                    "data_source": "city_baseline",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a multi-country Ava Home training CSV from implemented official sources."
    )
    parser.add_argument("--france-year", type=int, default=2024)
    parser.add_argument("--france-rows", type=int, default=50_000)
    parser.add_argument("--baseline-rows-per-city", type=int, default=24)
    parser.add_argument("--no-baselines", action="store_true")
    args = parser.parse_args()

    sources = pd.read_csv(SOURCE_REGISTRY_PATH)
    implemented = sources[sources["status"] == "implemented"]
    print("Implemented sources:")
    print(implemented[["country", "source_name", "training_value"]].to_string(index=False))

    targets = pd.read_csv(CITY_TARGETS_PATH)
    print(f"European target city list contains {len(targets)} cities.")

    frames = [build_france(year=args.france_year, max_rows=args.france_rows)]
    if not args.no_baselines:
        baseline_data = build_city_baselines(rows_per_city=args.baseline_rows_per_city)
        print(f"Generated {len(baseline_data):,} European city baseline rows.")
        frames.append(baseline_data)
    data = pd.concat(frames, ignore_index=True)

    model_columns = [
        "country_iso2",
        "country",
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
        "data_source",
        "price",
    ]
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    data[model_columns].to_csv(PROCESSED_PATH, index=False)

    country_counts_path = ROOT / "data" / "processed" / "country_source_counts.csv"
    data.groupby(["country_iso2", "country", "data_source"]).size().reset_index(name="rows").to_csv(
        country_counts_path, index=False
    )

    print(f"Saved {len(data):,} training rows to {PROCESSED_PATH}")
    print(f"Saved source counts to {country_counts_path}")


if __name__ == "__main__":
    main()
