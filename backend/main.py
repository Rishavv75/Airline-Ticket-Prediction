from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import FlightInput, PredictionResponse
from backend.services.predictor import (
    predict_price,
    MODEL_VERSION,
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Airline Ticket Price Prediction API",
    description=(
        "Machine learning API for predicting airline ticket prices."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTE NORMALIZATION
# ============================================================

def normalize_route(route: str) -> str:
    """
    Normalize route formatting so frontend/API input
    matches the representation used during model training.
    """

    if not route:
        return route

    route = route.replace("->", "→")

    parts = route.split("→")
    parts = [part.strip() for part in parts]

    return " → ".join(parts)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Airline Ticket Price Prediction API",
        "status": "running",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
    }


# ============================================================
# METADATA
# ============================================================

@app.get("/metadata")
def metadata():

    return {
        "airlines": [
            "Air India",
            "Air Asia",
            "GoAir",
            "IndiGo",
            "Jet Airways",
            "Jet Airways Business",
            "Multiple carriers",
            "Multiple carriers Premium economy",
            "SpiceJet",
            "Trujet",
            "Vistara",
            "Vistara Premium economy",
        ],

        "sources": [
            "Banglore",
            "Chennai",
            "Delhi",
            "Kolkata",
            "Mumbai",
        ],

        "destinations": [
            "Banglore",
            "Cochin",
            "Delhi",
            "Hyderabad",
            "Kolkata",
            "New Delhi",
        ],

        "stops": [
            "non-stop",
            "1 stop",
            "2 stops",
            "3 stops",
            "4 stops",
        ],

        "additional_info": [
            "No info",
            "In-flight meal not included",
            "No check-in baggage included",
            "1 Long layover",
            "Change airports",
            "Business class",
            "No Info",
            "1 Short layover",
            "Red-eye flight",
            "2 Long layover",
        ],
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(flight: FlightInput):

    try:

        # ----------------------------------------------------
        # NORMALIZE ROUTE
        # ----------------------------------------------------

        normalized_route = normalize_route(
            flight.route
        )

        # ----------------------------------------------------
        # DEBUG INFORMATION
        # ----------------------------------------------------

        print()
        print("==========================================")
        print("PREDICTION REQUEST")
        print("==========================================")
        print(f"Airline: {flight.airline}")
        print(f"Source: {flight.source}")
        print(f"Destination: {flight.destination}")
        print(f"Route received: {flight.route}")
        print(f"Route normalized: {normalized_route}")
        print(f"Departure: {flight.departure_time}")
        print(f"Arrival: {flight.arrival_time}")
        print(f"Duration: {flight.duration}")
        print(f"Stops: {flight.total_stops}")
        print(f"Additional Info: {flight.additional_info}")
        print("==========================================")

        # ----------------------------------------------------
        # API INPUT → MODEL INPUT
        # ----------------------------------------------------

        flight_data = {
            "Airline": flight.airline,
            "Date_of_Journey": flight.date_of_journey,
            "Source": flight.source,
            "Destination": flight.destination,
            "Route": normalized_route,
            "Dep_Time": flight.departure_time,
            "Arrival_Time": flight.arrival_time,
            "Duration": flight.duration,
            "Total_Stops": flight.total_stops,
            "Additional_Info": flight.additional_info,
        }

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        predicted_price = predict_price(
            flight_data
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return PredictionResponse(
            predicted_price=round(
                predicted_price,
                2,
            ),
            currency="INR",
            model="Random Forest",
            model_version=MODEL_VERSION,
        )

    except Exception as e:

        print()
        print("==========================================")
        print("PREDICTION ERROR")
        print("==========================================")
        print(str(e))
        print("==========================================")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )