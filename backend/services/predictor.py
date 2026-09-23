from pathlib import Path

import joblib
import pandas as pd

from ml.src.features import engineer_features


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "final_pipeline.joblib"
)


MODEL_VERSION = "1.0"


# ============================================================
# LOAD MODEL
# ============================================================

print("==========================================")
print("LOADING ML MODEL")
print("==========================================")
print(f"Model path: {MODEL_PATH}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"ML model not found at: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

print("ML model loaded successfully.")
print("==========================================")


# ============================================================
# PREDICTION
# ============================================================

def predict_price(flight_data: dict) -> float:
    """
    Convert raw API input into the same feature
    representation used during model training
    and generate a ticket price prediction.
    """

    # --------------------------------------------------------
    # RAW INPUT → DATAFRAME
    # --------------------------------------------------------

    df = pd.DataFrame([flight_data])

    # --------------------------------------------------------
    # FEATURE ENGINEERING
    # --------------------------------------------------------

    df = engineer_features(df)

    # --------------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(df)

    return float(prediction[0])