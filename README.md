# Ava Home

Ava Home is the property-price estimation module for the wider Ava ecosystem.

The first target is a professional backend foundation:

- FastAPI API
- Home price prediction endpoint
- ML training scripts
- PostgreSQL-ready database models
- Docker deployment structure
- Website and mobile placeholders

## Project Structure

```text
ava-home/
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- routes/
|   |   |   |-- health.py
|   |   |   `-- home.py
|   |   |-- schemas/
|   |   |   `-- home_schema.py
|   |   |-- services/
|   |   |   `-- prediction_service.py
|   |   |-- database/
|   |   |   |-- connection.py
|   |   |   `-- models.py
|   |   `-- ml/
|   |-- requirements.txt
|   |-- Dockerfile
|   `-- .env.example
|-- data/
|   |-- raw/
|   |   `-- houses.csv
|   `-- processed/
|-- training/
|   |-- clean_data.py
|   `-- train_model.py
|-- frontend/
|   `-- ava-home-web/
|-- mobile/
|   `-- ava-mobile/
|-- docker-compose.yml
`-- README.md
```

## Run Locally

```powershell
cd C:\Users\Ali\Documents\Codex\ava-home
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend\requirements.txt
python training\clean_data.py
python training\train_model.py
cd backend
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## First API Target

Endpoint:

```text
POST /api/home/predict
```

Example request:

```json
{
  "surface": 80,
  "rooms": 4,
  "bedrooms": 3,
  "city": "Lyon",
  "garage": 1,
  "balcony": 1,
  "garden": 0,
  "year": 2010,
  "condition": "good"
}
```

Example response:

```json
{
  "predicted_price": 315000,
  "currency": "EUR",
  "confidence_score": 0.72,
  "message": "Prediction completed successfully"
}
```

## Build Training Data From Official DVF Data

The project includes a data builder for the official French DVF open dataset.

```powershell
cd C:\Users\Ali\Documents\Codex\ava-home
.\.venv\Scripts\activate
python training\build_dvf_dataset.py --year 2024 --max-rows 50000
python training\train_model.py
```

This writes:

```text
data/processed/houses_clean.csv
backend/app/ml/house_price_model.pkl
```

Large downloaded raw files are ignored by Git.

## European Training Expansion

The project includes a European target-city list and source registry:

```text
data/reference/europe_city_targets.csv
data/reference/europe_property_sources.csv
```

Build the currently implemented European dataset:

```powershell
python training\build_europe_dataset.py --france-year 2024 --france-rows 50000
python training\train_model.py
```

Only France/DVF is implemented today. Other countries require official source connectors or API access before they can be used in the same model.

## Docker

Create `backend/.env` from `backend/.env.example`, then:

```powershell
docker compose up -d --build
```

## Android Mobile App

The first Android prototype lives in:

```text
mobile/ava-mobile
```

Open that folder in Android Studio, then run the `app` configuration. The first version includes:

- Welcome screen
- Property input form
- Local estimated price result
- Saved prediction history
- Settings screen

Command-line debug build:

```powershell
cd C:\Users\Ali\Documents\Codex\ava-home\mobile\ava-mobile
$env:JAVA_HOME='C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :app:assembleDebug
```

## Roadmap

1. Build Ava Home API with FastAPI
2. Train simple ML model
3. Store predictions in PostgreSQL
4. Deploy on Hetzner
5. Connect `api.avaintelligent.info`
6. Add Ava Home form to website
7. Build mobile screen
8. Add News, Electric, and Fuel links
9. Create Ava Living Score
10. Monetize with premium reports and partnerships
