# Ava Home Data

## Current Training Source

The first real training pipeline uses the official French DVF open-data dataset:

- Source: data.gouv.fr, "Demandes de valeurs foncieres"
- Dataset page: https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres/
- Current builder script: `training/build_dvf_dataset.py`
- Generated model input: `data/processed/houses_clean.csv`

The script downloads a yearly DVF ZIP file into `data/raw/`, extracts property transactions, and normalizes them into the Ava Home model columns:

```text
surface, rooms, bedrooms, city, postal_code, garage, balcony, garden, year, condition, price
```

## Legal / Data Protection Note

DVF is public/open data, but the reuse rules warn against re-identifying people or building personal-data indexes. Ava Home keeps only property-level training fields and does not store owner names or personal identifiers.

## Current Limitations

This is a first baseline dataset. DVF rows can represent complex sales with multiple lots, and some useful listing features are not available directly, such as exact condition, balcony, garage, and renovation quality. The first model is therefore useful for technical validation, but not yet a production-grade valuation engine.

Recommended next improvements:

- Aggregate complex mutations more carefully.
- Add geospatial features from postal code or city coordinates.
- Add market indicators by city and quarter.
- Train per-country models when additional official datasets are added.
- Consider gradient boosting models after the baseline Random Forest.
