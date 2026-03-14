import pandas as pd
from airflow.models import Variable
from sqlalchemy import create_engine

def load_taxi_model(**context):
    """
    Airflow PythonOperator function to load transformed taxi data
    into a MySQL star-schema data warehouse.
    """

    # Get Airflow Task Instance
    ti = context['ti']

    # Pull transformed CSV path from XCom
    transform_path = ti.xcom_pull(
        key="transformed_path",
        task_ids="transform_taxi_data"
    )

    print(f"Loading transformed data from: {transform_path}")

    # Load CSV file
    df = pd.read_csv(transform_path)

    # Get MySQL credentials from Airflow Variables
    host = Variable.get("MYSQL_HOST")
    user = Variable.get("MYSQL_USER")
    password = Variable.get("MYSQL_PASS")
    db = Variable.get("MYSQL_DB")

    # Create SQLAlchemy connection
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{db}"
    )

    # -----------------------------
    # Create Dimension Tables
    # -----------------------------

    dim_time = df[[
        'pickup_hour',
        'pickup_day_of_week',
        'is_weekend'
    ]].drop_duplicates()

    dim_payment = df[['payment_type']].drop_duplicates()

    # -----------------------------
    # Create Fact Table
    # -----------------------------

    fact_trips = df[[
        'pickup_hour',
        'pickup_day_of_week',
        'is_weekend',
        'payment_type',
        'fare_amount',
        'trip_distance',
        'trip_duration_minutes',
        'speed_mph',
        'fare_per_mile',
        'passenger_count'
    ]]

    # -----------------------------
    # Write tables to MySQL
    # -----------------------------

    dim_time.to_sql(
        "dim_time",
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )

    dim_payment.to_sql(
        "dim_payment",
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )

    fact_trips.to_sql(
        "fact_trips",
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )

    # -----------------------------
    # Logging
    # -----------------------------

    print("dim_time rows:", len(dim_time))
    print("dim_payment rows:", len(dim_payment))
    print("fact_trips rows:", len(fact_trips))

    return "Load completed"