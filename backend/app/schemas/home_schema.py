from pydantic import BaseModel, Field


class HomePredictionInput(BaseModel):
    surface: float = Field(..., gt=0, description="Property surface in square meters")
    rooms: int = Field(..., ge=1)
    bedrooms: int = Field(..., ge=0)
    city: str = Field(..., min_length=1)
    postal_code: str | None = None
    garage: int = Field(default=0, ge=0, le=1)
    balcony: int = Field(default=0, ge=0, le=1)
    garden: int = Field(default=0, ge=0, le=1)
    year: int = Field(..., ge=1800, le=2100)
    condition: str = "good"


class HomePredictionOutput(BaseModel):
    predicted_price: float
    currency: str = "EUR"
    confidence_score: float
    message: str
