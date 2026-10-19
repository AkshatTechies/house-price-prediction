# backend/schemas.py
from pydantic import BaseModel, Field, field_validator

class HouseFeatures(BaseModel):
    area: float = Field(gt=100, le=100_000, description="Built-up area in square feet")
    bedrooms: int = Field(ge=1, le=20)
    bathrooms: int = Field(ge=1, le=20)
    location: str = Field(min_length=2, max_length=100)
    age_years: int = Field(ge=0, le=150)
    location_score: float = Field(default=50.0, ge=0, le=100)

    @field_validator("location")
    @classmethod
    def normalize_location(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("location cannot be blank")
        return value

class PredictionResponse(BaseModel):
    predicted_price: float = Field(ge=0)
    currency: str = "INR"
