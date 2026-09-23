from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from features import engineer_features


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "flights.xlsx"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "ml"
    / "models"
)

MODEL_PATH = (
    MODEL_DIR
    / "final_pipeline.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_excel(DATA_PATH)

print(
    f"Raw dataset shape: {df.shape}"
)


# ============================================================
# FEATURE ENGINEERING
# ============================================================

print("\nEngineering features...")

df = engineer_features(df)

print(
    f"Processed dataset shape: {df.shape}"
)


# ============================================================
# REMOVE INVALID ROWS
# ============================================================

df = df.dropna()

print(
    f"Dataset after cleaning: {df.shape}"
)


# ============================================================
# TARGET
# ============================================================

X = df.drop(
    columns=["Price"]
)

y = df["Price"]


# ============================================================
# FEATURE GROUPS
# ============================================================

categorical_features = [
    "Airline",
    "Source",
    "Destination",
    "Route",
    "Additional_Info"
]

numerical_features = [
    "Total_Stops",
    "Journey_Day",
    "Journey_Month",
    "Journey_Weekday",
    "Departure_Hour",
    "Departure_Minute",
    "Arrival_Hour",
    "Arrival_Minute",
    "Duration_Minutes",
    "Departure_Time_Minutes",
    "Arrival_Time_Minutes",
    "Is_Weekend",
    "Is_Night_Flight"
]


# ============================================================
# PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# RANDOM FOREST
# ============================================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# COMPLETE PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\nTraining final Random Forest pipeline...")

pipeline.fit(
    X_train,
    y_train
)


print("Training completed.")


# ============================================================
# SAVE
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    pipeline,
    MODEL_PATH
)


print("\n==========================================")
print("FINAL MODEL SAVED")
print("==========================================")

print(
    MODEL_PATH
)