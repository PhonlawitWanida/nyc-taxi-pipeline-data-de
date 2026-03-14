
import pandas as pd
import logging

def clean_taxi_data(**context):
    ti = context["ti"]

    raw_path = ti.xcom_pull(
        key="raw_path",
        task_ids="ingest_taxi_data"
    )

    logging.info(f"Loading raw data from: {raw_path}")

    df = pd.read_csv(raw_path)

    original_rows = len(df)

    # Remove invalid fare amounts
    df = df[(df["fare_amount"] > 0) & (df["fare_amount"] <= 500)]
    logging.info(f"After fare filter: {len(df)} rows remaining")

    # Remove invalid trip distances
    df = df[(df["trip_distance"] > 0) & (df["trip_distance"] <= 100)]
    logging.info(f"After distance filter: {len(df)} rows remaining")

    # Remove invalid coordinates
    if {"pickup_latitude","pickup_longitude","dropoff_latitude","dropoff_longitude"}.issubset(df.columns):
        df = df[
            (df["pickup_latitude"].between(40.4, 41.0)) &
            (df["dropoff_latitude"].between(40.4, 41.0)) &
            (df["pickup_longitude"].between(-74.3, -73.5)) &
            (df["dropoff_longitude"].between(-74.3, -73.5))
        ]
        logging.info(f"After coordinate filter: {len(df)} rows remaining")

    # Drop null values
    df = df.dropna(subset=["fare_amount", "trip_distance", "tpep_pickup_datetime"])
    logging.info(f"After null removal: {len(df)} rows remaining")

    # Parse datetime
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")

    cleaned_rows = len(df)
    logging.info(f"Total rows removed: {original_rows - cleaned_rows}")

    output_path = "/tmp/nyc_taxi_clean.csv"
    df.to_csv(output_path, index=False)

    logging.info(f"Cleaned dataset saved to: {output_path}")

    ti.xcom_push(key="clean_path", value=output_path)

    return output_path
