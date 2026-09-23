from pathlib import Path

import joblib
import pandas as pd

from features import engineer_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "flights.xlsx"

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "xgboost_model.joblib"


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_excel(DATA_PATH)

df = engineer_features(df)


X = df.drop(columns=["Price"])


# ============================================================
# LOAD MODEL
# ============================================================

artifact = joblib.load(MODEL_PATH)

preprocessor = artifact["preprocessor"]

model = artifact["model"]


# ============================================================
# GET FEATURE NAMES
# ============================================================

feature_names = preprocessor.get_feature_names_out()


# ============================================================
# GET IMPORTANCE
# ============================================================

importances = model.feature_importances_


importance_df = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": importances
    }
)


importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
)


# ============================================================
# DISPLAY
# ============================================================

print("\n==============================")
print("TOP 30 FEATURE IMPORTANCES")
print("==============================")

print(
    importance_df.head(30).to_string(
        index=False
    )
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "feature_importance.csv"
)

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

importance_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nFeature importance saved to:")
print(OUTPUT_PATH)