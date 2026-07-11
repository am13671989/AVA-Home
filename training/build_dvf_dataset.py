from __future__ import annotations

import argparse
import csv
import io
import re
import zipfile
from pathlib import Path
from urllib.request import urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_PATH = ROOT / "data" / "processed" / "houses_clean.csv"

DVF_URLS = {
    2025: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20260405-002321/valeursfoncieres-2025.txt.zip",
    2024: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20260405-002306/valeursfoncieres-2024.txt.zip",
    2023: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20260405-002251/valeursfoncieres-2023.txt.zip",
    2022: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20260405-002236/valeursfoncieres-2022.txt.zip",
    2021: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20260405-002223/valeursfoncieres-2021.txt.zip",
}

CITY_COLUMN = "Commune"
POSTAL_COLUMN = "Code postal"
PRICE_COLUMN = "Valeur fonciere"
SURFACE_COLUMN = "Surface reelle bati"
ROOMS_COLUMN = "Nombre pieces principales"
PROPERTY_TYPE_COLUMN = "Type local"
DATE_COLUMN = "Date mutation"


def download_year(year: int) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / f"valeursfoncieres-{year}.txt.zip"
    if target.exists() and target.stat().st_size > 0:
        return target

    url = DVF_URLS[year]
    print(f"Downloading official DVF {year} data...")
    with urlopen(url, timeout=120) as response, target.open("wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
    return target


def _money_to_float(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip().replace(" ", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def _clean_postal_code(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    digits = re.sub(r"\D", "", text)
    return digits.zfill(5)[:5] if digits else ""


def _normalize_dvf_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    required = [
        CITY_COLUMN,
        POSTAL_COLUMN,
        PRICE_COLUMN,
        SURFACE_COLUMN,
        ROOMS_COLUMN,
        PROPERTY_TYPE_COLUMN,
        DATE_COLUMN,
    ]
    chunk = chunk[[column for column in required if column in chunk.columns]].copy()
    chunk = chunk[chunk[PROPERTY_TYPE_COLUMN].isin(["Appartement", "Maison"])]

    chunk["price"] = chunk[PRICE_COLUMN].map(_money_to_float)
    chunk["surface"] = pd.to_numeric(chunk[SURFACE_COLUMN], errors="coerce")
    chunk["rooms"] = pd.to_numeric(chunk[ROOMS_COLUMN], errors="coerce")
    chunk["city"] = chunk[CITY_COLUMN].fillna("").astype(str).str.title().str.strip()
    chunk["postal_code"] = chunk[POSTAL_COLUMN].map(_clean_postal_code)
    chunk["year"] = pd.to_datetime(chunk[DATE_COLUMN], dayfirst=True, errors="coerce").dt.year

    chunk = chunk.dropna(subset=["price", "surface", "rooms", "year"])
    chunk = chunk[
        (chunk["price"].between(20_000, 5_000_000))
        & (chunk["surface"].between(10, 500))
        & (chunk["rooms"].between(1, 12))
        & (chunk["city"] != "")
    ]

    normalized = pd.DataFrame(
        {
            "surface": chunk["surface"].round().astype(int),
            "rooms": chunk["rooms"].round().astype(int),
            "bedrooms": (chunk["rooms"] - 1).clip(lower=0).round().astype(int),
            "city": chunk["city"],
            "postal_code": chunk["postal_code"],
            "garage": 0,
            "balcony": 0,
            "garden": (chunk[PROPERTY_TYPE_COLUMN] == "Maison").astype(int),
            "year": chunk["year"].astype(int),
            "condition": "good",
            "price": chunk["price"].round().astype(int),
        }
    )
    return normalized.drop_duplicates()


def build_dataset(year: int, max_rows: int, chunksize: int) -> pd.DataFrame:
    zip_path = download_year(year)
    frames: list[pd.DataFrame] = []
    collected = 0

    with zipfile.ZipFile(zip_path) as archive:
        txt_name = next(name for name in archive.namelist() if name.endswith(".txt"))
        with archive.open(txt_name) as raw:
            text_stream = io.TextIOWrapper(raw, encoding="utf-8", errors="replace")
            reader = pd.read_csv(
                text_stream,
                sep="|",
                dtype=str,
                chunksize=chunksize,
                quoting=csv.QUOTE_NONE,
                low_memory=False,
            )
            for chunk in reader:
                normalized = _normalize_dvf_chunk(chunk)
                if not normalized.empty:
                    frames.append(normalized)
                    collected += len(normalized)
                print(f"Collected {collected:,} usable rows...")
                if collected >= max_rows:
                    break

    if not frames:
        raise RuntimeError("No usable rows were collected from the DVF dataset.")

    data = pd.concat(frames, ignore_index=True).drop_duplicates()
    return data.head(max_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Ava Home training CSV from official French DVF open data.")
    parser.add_argument("--year", type=int, default=2024, choices=sorted(DVF_URLS.keys()))
    parser.add_argument("--max-rows", type=int, default=50_000)
    parser.add_argument("--chunksize", type=int, default=100_000)
    args = parser.parse_args()

    data = build_dataset(args.year, args.max_rows, args.chunksize)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved {len(data):,} rows to {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
