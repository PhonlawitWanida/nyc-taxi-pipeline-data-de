import pandas as pd

def transform_taxi_data(**context):
    """
    Airflow PythonOperator function for transforming NYC Taxi data
    """

    # Get Airflow Task Instance
    ti = context['ti']

    # 1. Pull cleaned CSV path from XCom
    clean_path = ti.xcom_pull(
        key="clean_path",
        task_ids="clean_taxi_data"
    )

    print(f"Loading cleaned data from: {clean_path}")

    # 2. Load cleaned dataset
    df = pd.read_csv(clean_path)

    # Convert datetime columns
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    # ---------------------------
    # Feature Engineering
    # ---------------------------

    # Trip duration (minutes)
    df["trip_duration_minutes"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    # Speed mph
    df["speed_mph"] = df["trip_distance"] / (df["trip_duration_minutes"] / 60)

    # Fare per mile
    df["fare_per_mile"] = df["fare_amount"] / df["trip_distance"]

    # Pickup hour
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour

    # Day of week
    df["pickup_day_of_week"] = df["tpep_pickup_datetime"].dt.weekday

    # Weekend flag
    df["is_weekend"] = df["pickup_day_of_week"] >= 5

    # ---------------------------
    # Filter unrealistic trips
    # ---------------------------

    df = df[
        (df["speed_mph"] <= 80) &
        (df["trip_duration_minutes"] >= 1)
    ]

    # ---------------------------
    # Save transformed dataset
    # ---------------------------

    output_path = "/tmp/nyc_taxi_transformed.csv"

    df.to_csv(output_path, index=False)

    print(f"Transformed data saved to: {output_path}")

    # ---------------------------
    # Push path to XCom
    # ---------------------------

    ti.xcom_push(
        key="transformed_path",
        value=output_path
    )

    # ---------------------------
    # Print statistics
    # ---------------------------

    stats = df[[
        "trip_duration_minutes",
        "speed_mph",
        "fare_per_mile"
    ]].describe()

    print("Descriptive statistics:")
    print(stats)

    return output_path