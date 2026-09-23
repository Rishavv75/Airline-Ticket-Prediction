from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from features import engineer_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "flights.xlsx"

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "xgboost_model.joblib"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_excel(DATA_PATH)

df = engineer_features(df)


# ============================================================
# FEATURES / TARGET
# ============================================================

X = df.drop(columns=["Price"])
y = df["Price"]


# ============================================================
# SAME SPLIT AS TRAINING
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading trained XGBoost model...")

artifact = joblib.load(MODEL_PATH)

preprocessor = artifact["preprocessor"]
model = artifact["model"]


# ============================================================
# TRANSFORM TEST DATA
# ============================================================

X_test_transformed = preprocessor.transform(X_test)


# ============================================================
# PREDICTIONS
# ============================================================

y_pred = model.predict(X_test_transformed)


# ============================================================
# METRICS
# ============================================================

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)


print("\n==============================")
print("XGBOOST VALIDATION")
print("==============================")

print(f"MAE  : ₹{mae:,.2f}")
print(f"RMSE : ₹{rmse:,.2f}")
print(f"R²   : {r2:.4f}")


# ============================================================
# ERROR ANALYSIS
# ============================================================

results = X_test.copy()

results["Actual_Price"] = y_test.values

results["Predicted_Price"] = y_pred

results["Absolute_Error"] = (
    results["Actual_Price"] -
    results["Predicted_Price"]
).abs()

results["Percentage_Error"] = (
    results["Absolute_Error"] /
    results["Actual_Price"]
) * 100


# ============================================================
# LARGEST ERRORS
# ============================================================

print("\n==============================")
print("LARGEST PREDICTION ERRORS")
print("==============================")

largest_errors = results.sort_values(
    "Absolute_Error",
    ascending=False
)

print(
    largest_errors[
        [
            "Airline",
            "Source",
            "Destination",
            "Route",
            "Total_Stops",
            "Actual_Price",
            "Predicted_Price",
            "Absolute_Error",
            "Percentage_Error"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# SAVE ERROR ANALYSIS
# ============================================================

OUTPUT_PATH = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "prediction_errors.csv"
)

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nError analysis saved to:")
print(OUTPUT_PATH)