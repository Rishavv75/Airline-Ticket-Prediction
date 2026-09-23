from pathlib import Path

import pandas as pd


# Project root:
# plane ticket prediction/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw dataset path
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "flights.xlsx"


def extract_date_features(df):
    df = df.copy()

    df["Date_of_Journey"] = pd.to_datetime(
        df["Date_of_Journey"],
        dayfirst=True
    )

    df["Journey_Day"] = df["Date_of_Journey"].dt.day
    df["Journey_Month"] = df["Date_of_Journey"].dt.month
    df["Journey_Weekday"] = df["Date_of_Journey"].dt.weekday

    df.drop(columns=["Date_of_Journey"], inplace=True)

    return df


def extract_departure_time(df):
    df = df.copy()

    df["Dep_Time"] = pd.to_datetime(
        df["Dep_Time"],
        format="%H:%M"
    )

    df["Departure_Hour"] = df["Dep_Time"].dt.hour
    df["Departure_Minute"] = df["Dep_Time"].dt.minute

    df.drop(columns=["Dep_Time"], inplace=True)

    return df


def extract_arrival_time(df):
    df = df.copy()

    df["Arrival_Hour"] = (
        df["Arrival_Time"]
        .str.extract(r"(\d{1,2}):")[0]
        .astype(int)
    )

    df["Arrival_Minute"] = (
        df["Arrival_Time"]
        .str.extract(r":(\d{2})")[0]
        .astype(int)
    )

    df.drop(columns=["Arrival_Time"], inplace=True)

    return df


def convert_duration_to_minutes(df):
    df = df.copy()

    def duration_to_minutes(duration):
        hours = 0
        minutes = 0

        parts = duration.split()

        for part in parts:
            if "h" in part:
                hours = int(part.replace("h", ""))

            elif "m" in part:
                minutes = int(part.replace("m", ""))

        return hours * 60 + minutes

    df["Duration_Minutes"] = df["Duration"].apply(
        duration_to_minutes
    )

    df.drop(columns=["Duration"], inplace=True)

    return df


def convert_stops(df):
    df = df.copy()

    stops_mapping = {
        "non-stop": 0,
        "1 stop": 1,
        "2 stops": 2,
        "3 stops": 3,
        "4 stops": 4
    }

    df["Total_Stops"] = df["Total_Stops"].map(stops_mapping)

    return df


def handle_missing_values(df):
    df = df.copy()

    # Remove rows where critical route information is missing.
    df = df.dropna(
        subset=["Route", "Total_Stops"]
    )

    # Fill non-critical categorical information.
    df["Additional_Info"] = df["Additional_Info"].fillna("Unknown")

    return df

def create_time_features(df):
    df = df.copy()

    # Departure time as minutes since midnight
    df["Departure_Time_Minutes"] = (
        df["Departure_Hour"] * 60
        + df["Departure_Minute"]
    )

    # Arrival time as minutes since midnight
    df["Arrival_Time_Minutes"] = (
        df["Arrival_Hour"] * 60
        + df["Arrival_Minute"]
    )

    # Weekend indicator
    df["Is_Weekend"] = (
        df["Journey_Weekday"] >= 5
    ).astype(int)

    # Night departure indicator
    df["Is_Night_Flight"] = (
        (df["Departure_Hour"] >= 22)
        | (df["Departure_Hour"] < 5)
    ).astype(int)

    return df

def engineer_features(df):
    df = handle_missing_values(df)

    df = extract_date_features(df)
    df = extract_departure_time(df)
    df = extract_arrival_time(df)
    df = convert_duration_to_minutes(df)
    df = convert_stops(df)
    df = create_time_features(df)

    return df


if __name__ == "__main__":
    print("Loading dataset...")

    df = pd.read_excel(DATA_PATH)

    print(f"Dataset loaded successfully: {df.shape}")

    print("\nEngineering features...")

    processed_df = engineer_features(df)

    print("\nFeature engineering completed successfully.")

    print("\nFirst 5 rows:")
    print(processed_df.head())

    print("\nColumns:")
    print(processed_df.columns.tolist())

    print("\nData types:")
    print(processed_df.dtypes)

    print("\nMissing values after feature engineering:")
    print(processed_df.isnull().sum())