from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error

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

RF_MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "baseline_random_forest.joblib"
)

XGB_MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "xgboost_model.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_excel(DATA_PATH)

df = engineer_features(df)

print(f"Dataset shape: {df.shape}")


X = df.drop(columns=["Price"])

y = df["Price"]


# ============================================================
# SAME TEST SPLIT USED DURING TRAINING
# ============================================================

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ============================================================
# LOAD RANDOM FOREST ARTIFACT
# ============================================================

print("\nLoading Random Forest...")

rf_artifact = joblib.load(RF_MODEL_PATH)

print("Random Forest artifact type:")
print(type(rf_artifact))


# ============================================================
# LOAD XGBOOST ARTIFACT
# ============================================================

print("\nLoading XGBoost...")

xgb_artifact = joblib.load(XGB_MODEL_PATH)

print("XGBoost artifact type:")
print(type(xgb_artifact))


# ============================================================
# EXTRACT MODEL + PREPROCESSOR
# ============================================================

if isinstance(rf_artifact, dict):

    rf_model = rf_artifact["model"]
    rf_preprocessor = rf_artifact["preprocessor"]

else:

    raise ValueError(
        "Random Forest artifact does not contain "
        "'model' and 'preprocessor'."
    )


if isinstance(xgb_artifact, dict):

    xgb_model = xgb_artifact["model"]
    xgb_preprocessor = xgb_artifact["preprocessor"]

else:

    raise ValueError(
        "XGBoost artifact does not contain "
        "'model' and 'preprocessor'."
    )


# ============================================================
# TRANSFORM USING THE ORIGINAL TRAINED PREPROCESSORS
# ============================================================

print("\nTransforming test data...")

X_test_rf = rf_preprocessor.transform(
    X_test
)

X_test_xgb = xgb_preprocessor.transform(
    X_test
)


print(
    "Random Forest transformed shape:",
    X_test_rf.shape
)

print(
    "XGBoost transformed shape:",
    X_test_xgb.shape
)


# ============================================================
# PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

rf_pred = rf_model.predict(
    X_test_rf
)

xgb_pred = xgb_model.predict(
    X_test_xgb
)


# ============================================================
# RESULTS DATAFRAME
# ============================================================

results = pd.DataFrame(
    {
        "Actual_Price": y_test.values,
        "Random_Forest": rf_pred,
        "XGBoost": xgb_pred
    }
)


# ============================================================
# PRICE RANGES
# ============================================================

bins = [
    0,
    5000,
    10000,
    20000,
    40000,
    np.inf
]

labels = [
    "< ₹5K",
    "₹5K–₹10K",
    "₹10K–₹20K",
    "₹20K–₹40K",
    "> ₹40K"
]

results["Price_Range"] = pd.cut(
    results["Actual_Price"],
    bins=bins,
    labels=labels,
    right=False
)


# ============================================================
# EVALUATION
# ============================================================

print("\n==========================================")
print("PERFORMANCE BY PRICE RANGE")
print("==========================================")


for price_range in labels:

    subset = results[
        results["Price_Range"] == price_range
    ]

    if len(subset) == 0:
        continue

    print(
        f"\n{price_range}"
    )

    print(
        f"Samples: {len(subset)}"
    )


    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    rf_mae = mean_absolute_error(
        subset["Actual_Price"],
        subset["Random_Forest"]
    )

    rf_rmse = np.sqrt(
        mean_squared_error(
            subset["Actual_Price"],
            subset["Random_Forest"]
        )
    )


    # --------------------------------------------------------
    # XGBOOST
    # --------------------------------------------------------

    xgb_mae = mean_absolute_error(
        subset["Actual_Price"],
        subset["XGBoost"]
    )

    xgb_rmse = np.sqrt(
        mean_squared_error(
            subset["Actual_Price"],
            subset["XGBoost"]
        )
    )


    print(
        f"Random Forest | "
        f"MAE: ₹{rf_mae:,.2f} | "
        f"RMSE: ₹{rf_rmse:,.2f}"
    )

    print(
        f"XGBoost       | "
        f"MAE: ₹{xgb_mae:,.2f} | "
        f"RMSE: ₹{xgb_rmse:,.2f}"
    )


# ============================================================
# SAVE RESULTS
# ============================================================

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "price_range_evaluation.csv"
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n==========================================")
print("Evaluation completed.")
print("Results saved to:")
print(OUTPUT_PATH)
print("==========================================")