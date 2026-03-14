import requests
import pandas as pd
import logging
import time

def ingest_taxi_data(**context):

    url = "https://data.cityofnewyork.us/resource/t29m-gskq.csv?$limit=1000"
    output_path = "/tmp/nyc_taxi_raw.csv"

    logging.info("Downloading NYC taxi data")

    df = pd.read_csv(url)

    row_count = len(df)
    logging.info(f"Downloaded rows: {row_count}")

    if row_count < 100:
        raise ValueError("Dataset validation failed")

    df.to_csv(output_path, index=False)

    ti = context["ti"]
    ti.xcom_push(key="raw_path", value=output_path)

    return output_path