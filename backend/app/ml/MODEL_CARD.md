# Ava Home Price Model

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
