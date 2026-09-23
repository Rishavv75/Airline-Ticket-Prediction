from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor

from features import engineer_features


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "flights.xlsx"

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_PATH = MODEL_DIR / "xgboost_model.joblib"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_excel(DATA_PATH)

print(f"Raw dataset shape: {df.shape}")


# ============================================================
# FEATURE ENGINEERING
# ============================================================

print("\nEngineering features...")

df = engineer_features(df)

print(f"Processed dataset shape: {df.shape}")


# ============================================================
# FEATURES / TARGET
# ============================================================

X = df.drop(columns=["Price"])

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
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTrain samples:", len(X_train))
print("Test samples:", len(X_test))


# ============================================================
# PREPROCESSING
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
# TRANSFORM
# ============================================================

print("\nFitting preprocessing pipeline...")

X_train_transformed = preprocessor.fit_transform(X_train)

X_test_transformed = preprocessor.transform(X_test)

print("Preprocessing completed.")


# ============================================================
# XGBOOST MODEL
# ============================================================

print("\nTraining XGBoost...")

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train_transformed,
    y_train
)

print("XGBoost training completed.")


# ============================================================
# PREDICTION
# ============================================================

print("\nGenerating predictions...")

y_pred = model.predict(X_test_transformed)


# ============================================================
# EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


print("\n==============================")
print("XGBOOST EVALUATION")
print("==============================")

print(f"MAE  : ₹{mae:,.2f}")
print(f"RMSE : ₹{rmse:,.2f}")
print(f"R²   : {r2:.4f}")


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

artifact = {
    "preprocessor": preprocessor,
    "model": model
}

joblib.dump(
    artifact,
    MODEL_PATH
)

print("\nModel saved to:")
print(MODEL_PATH)