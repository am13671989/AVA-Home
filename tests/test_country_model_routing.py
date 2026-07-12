import pytest

from app.schemas.home_schema import HomePredictionInput
from app.services.prediction_service import predict_home_price


def _input(country: str, iso2: str, city: str) -> HomePredictionInput:
    return HomePredictionInput(
        country=country,
        country_iso2=iso2,
        surface=80,
        rooms=3,
        bedrooms=2,
        city=city,
        postal_code="75001",
        garage=0,
        balcony=1,
        garden=0,
        year=2010,
        condition="good",
    )


def test_france_uses_only_france_dvf_model():
    result = predict_home_price(_input("France", "FR", "Paris"))
    assert result.predicted_price > 0
    assert "France DVF" in result.data_scope
    assert "DVF 2024" in result.message


def test_country_selection_has_priority_over_city_name():
    result = predict_home_price(_input("France", "FR", "Barcelona"))
    assert "France DVF" in result.data_scope


def test_unsupported_country_is_rejected():
    with pytest.raises(ValueError, match="only France and Spain"):
        predict_home_price(_input("Germany", "DE", "Berlin"))
