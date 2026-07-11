# Ava Home Price Model

## Current Model

- Algorithm: RandomForestRegressor
- Estimators: 80
- Max depth: 18
- Minimum samples per leaf: 3
- Training rows: 20,000
- Current implemented training source: France DVF official open property transaction data

## Input Features

```text
country_iso2, country, surface, rooms, bedrooms, city, garage, balcony, garden, year, condition
```

## Target

```text
price
```

## Current Metrics

The current model is a baseline, not a production valuation model.

```text
MAE: 91282.99
R2: 0.335
```

## Limitations

Only the France DVF connector is implemented so far. The European city list is ready, but additional countries still need source-specific connectors or licensed data access. DVF also lacks exact property condition, garage, balcony, and listing quality information, so some fields are currently approximated.
