from app.schemas.home_schema import HomePredictionInput
from app.services.prediction_service import predict_home_price


def _input(city: str) -> HomePredictionInput:
    return HomePredictionInput(
        country="Spain",
        country_iso2="ES",
        surface=90,
        rooms=4,
        bedrooms=3,
        city=city,
        postal_code="28001",
        garage=1,
        balcony=1,
        garden=0,
        year=2015,
        condition="good",
    )


def test_spanish_cities_use_same_barcelona_trained_model():
    madrid = predict_home_price(_input("Madrid"))
    valencia = predict_home_price(_input("Valencia"))
    assert madrid.predicted_price == valencia.predicted_price
    assert madrid.model_type == "RandomForestRegressor (log-target)"
    assert "Barcelona listings" in madrid.data_scope


def test_spain_prediction_is_positive_and_has_range():
    result = predict_home_price(_input("Seville"))
    assert result.predicted_price > 0
    assert result.price_range_low < result.predicted_price < result.price_range_high
    assert result.estimated_price_per_m2 > 0
