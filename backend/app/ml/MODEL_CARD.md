# Ava Home Price Model

## Country routing

Production predictions are routed by `country_iso2`. France (`FR`) and Spain
(`ES`) each load an independent Random Forest artifact. Unsupported countries
return HTTP 422 and are not offered in the Android application.

## France model

`france_house_price_model.pkl` is trained only on official 2024 French DVF
transactions sampled across the full national archive. It uses surface, rooms,
bedrooms, house/apartment signal, and a France-DVF city price-per-m² feature.
See `france_house_price_model_metadata.json` for current validation metrics and
limitations.

## Spain experimental model

`spain_house_price_model.pkl` is a separate log-target Random Forest trained on
9,946 filtered Barcelona property listings from the user-supplied experimental
dataset. It uses surface, bedrooms, parking, balcony/terrace, garden, build year,
and renovation status. Spain requests are routed to this model independently of
the selected Spanish city.

Holdout metrics: MAE EUR 143,946; median absolute error EUR 67,774; MAPE 33.48%;
R² 0.6664. The source contains asking prices rather than completed transactions,
and Barcelona-only data cannot validate accuracy elsewhere in Spain. Results
must therefore be labeled experimental, not professional valuations.

## Current Model

- Algorithm: RandomForestRegressor
- Estimators: 80
- Max depth: 18
- Minimum samples per leaf: 3
- Training rows: 23,096
- Current implemented training sources:
  - France DVF official open property transaction data
  - European city baseline price-per-square-meter rows for target cities

## Input Features

```text
country_iso2, country, surface, rooms, bedrooms, city, garage, balcony, garden, year, condition, data_source
```

## Target

```text
price
```

## Current Metrics

The current model is a baseline, not a production valuation model.

```text
MAE: 90450.70
R2: 0.590
```

## Limitations

France is currently the only implemented official property-level connector. Other European cities are covered by baseline price-per-square-meter rows until source-specific connectors or licensed APIs are added. DVF also lacks exact property condition, garage, balcony, and listing quality information, so some fields are currently approximated.
