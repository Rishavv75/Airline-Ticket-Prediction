from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold

from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder

from features import engineer_features


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "flights.xlsx"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_excel(DATA_PATH)

df = engineer_features(df)

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
# CROSS VALIDATION
# ============================================================

kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


rf_metrics = {
    "MAE": [],
    "RMSE": [],
    "R2": []
}

xgb_metrics = {
    "MAE": [],
    "RMSE": [],
    "R2": []
}


# ============================================================
# FOLD LOOP
# ============================================================

for fold, (train_idx, test_idx) in enumerate(
    kf.split(X),
    start=1
):

    print(f"\n========== FOLD {fold} ==========")

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]


    # --------------------------------------------------------
    # PREPROCESSOR
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # FIT TRANSFORMER ONLY ON TRAINING FOLD
    # --------------------------------------------------------

    X_train_transformed = preprocessor.fit_transform(
        X_train
    )

    X_test_transformed = preprocessor.transform(
        X_test
    )


    # ========================================================
    # RANDOM FOREST
    # ========================================================

    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    rf.fit(
        X_train_transformed,
        y_train
    )

    rf_pred = rf.predict(
        X_test_transformed
    )


    rf_mae = mean_absolute_error(
        y_test,
        rf_pred
    )

    rf_rmse = mean_squared_error(
        y_test,
        rf_pred
    ) ** 0.5

    rf_r2 = r2_score(
        y_test,
        rf_pred
    )


    rf_metrics["MAE"].append(rf_mae)
    rf_metrics["RMSE"].append(rf_rmse)
    rf_metrics["R2"].append(rf_r2)


    # ========================================================
    # XGBOOST
    # ========================================================

    xgb = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1
    )

    xgb.fit(
        X_train_transformed,
        y_train
    )

    xgb_pred = xgb.predict(
        X_test_transformed
    )


    xgb_mae = mean_absolute_error(
        y_test,
        xgb_pred
    )

    xgb_rmse = mean_squared_error(
        y_test,
        xgb_pred
    ) ** 0.5

    xgb_r2 = r2_score(
        y_test,
        xgb_pred
    )


    xgb_metrics["MAE"].append(xgb_mae)
    xgb_metrics["RMSE"].append(xgb_rmse)
    xgb_metrics["R2"].append(xgb_r2)


    print(
        f"Random Forest | "
        f"MAE: ₹{rf_mae:,.2f} | "
        f"RMSE: ₹{rf_rmse:,.2f} | "
        f"R²: {rf_r2:.4f}"
    )

    print(
        f"XGBoost       | "
        f"MAE: ₹{xgb_mae:,.2f} | "
        f"RMSE: ₹{xgb_rmse:,.2f} | "
        f"R²: {xgb_r2:.4f}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n\n==========================================")
print("5-FOLD CROSS-VALIDATION RESULTS")
print("==========================================")


def print_summary(name, metrics):

    print(f"\n{name}")

    for metric, values in metrics.items():

        mean = np.mean(values)
        std = np.std(values)

        print(
            f"{metric:5s}: "
            f"{mean:.4f} ± {std:.4f}"
        )


print_summary(
    "Random Forest",
    rf_metrics
)

print_summary(
    "XGBoost",
    xgb_metrics
)