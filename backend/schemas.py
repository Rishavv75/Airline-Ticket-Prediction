from pydantic import BaseModel, Field


class FlightInput(BaseModel):
    airline: str = Field(..., min_length=1)
    date_of_journey: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    route: str = Field(..., min_length=1)
    departure_time: str = Field(..., min_length=1)
    arrival_time: str = Field(..., min_length=1)
    duration: str = Field(..., min_length=1)
    total_stops: str = Field(..., min_length=1)
    additional_info: str = Field(..., min_length=1)


class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str
    model: str
    model_version: str