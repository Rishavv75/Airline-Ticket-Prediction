from pathlib import Path

import pandas as pd

from features import engineer_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "flights.xlsx"


df = pd.read_excel(DATA_PATH)

df = engineer_features(df)


print("\n==============================")
print("AIRLINE STATISTICS")
print("==============================")

airline_stats = (
    df.groupby("Airline")["Price"]
    .agg(
        Count="count",
        Mean="mean",
        Median="median",
        Min="min",
        Max="max"
    )
    .sort_values("Count")
)

print(airline_stats.to_string())


print("\n==============================")
print("ADDITIONAL INFO STATISTICS")
print("==============================")

info_stats = (
    df.groupby("Additional_Info")["Price"]
    .agg(
        Count="count",
        Mean="mean",
        Median="median",
        Min="min",
        Max="max"
    )
    .sort_values("Count")
)

print(info_stats.to_string())


print("\n==============================")
print("JET AIRWAYS BUSINESS RECORDS")
print("==============================")

business = df[
    df["Airline"] == "Jet Airways Business"
]

print(
    business[
        [
            "Airline",
            "Source",
            "Destination",
            "Route",
            "Total_Stops",
            "Duration_Minutes",
            "Additional_Info",
            "Price"
        ]
    ].to_string(index=False)
)