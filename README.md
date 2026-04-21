# 🚕 NYC Taxi Data Pipeline with Apache Airflow

## 📌 Project Overview

This project implements a **data engineering pipeline** for processing NYC taxi trip data using **Apache Airflow**.
The pipeline ingests raw taxi data, cleans and transforms the dataset, and loads the processed data into a data warehouse.

The workflow is orchestrated using Airflow DAGs to automate each step of the ETL process.

---

# 🏗️ Pipeline Architecture

The ETL pipeline follows four main stages:

```
Ingest → Clean → Transform → Load
```

1. **Ingest**

   * Download raw NYC taxi trip data
   * Store the raw dataset

2. **Clean**

   * Remove invalid or missing values
   * Filter unrealistic trips

3. **Transform**

   * Create derived features such as trip duration and speed
   * Perform feature engineering

4. **Load**

   * Load the processed data into a MySQL data warehouse
   * Build fact and dimension tables

---

# ⚙️ Technologies Used

* **Python**
* **Apache Airflow**
* **Docker**
* **MySQL**
* **Pandas**
* **Git & GitHub**

---

# 📂 Project Structure

```
nyc-taxi-pipeline-data-de
│
├── dags
│   ├── ingest_taxi_data.py
│   ├── clean_taxi_data.py
│   ├── transform_taxi_data_airflow.py
│   ├── load_taxi_model_airflow.py
│   └── taxi_pipeline_dag.py
│
├── docker-compose.yaml
└── README.md
```

---

# 🔄 Airflow Workflow

The Airflow DAG executes tasks in the following order:

```
ingest_taxi_data
        ↓
clean_taxi_data
        ↓
transform_taxi_data
        ↓
load_taxi_model
```

Each task passes data between stages using **Airflow XCom**.
<img width="1919" height="941" alt="image" src="https://github.com/user-attachments/assets/f056d3e9-32ad-4273-9bf7-e42061a4d0b9" />

---

# 👥 Team Responsibilities

| Member   | Task                               |
| -------- | ---------------------------------- |
| PANNATHORN (175) | Data Ingestion                     |
| PHONLAWIT (584) | Data Cleaning                      |
| PHONRAWAT (249) | Data Transformation & Data Loading |

---

# ▶️ How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/PhonlawitWanida/nyc-taxi-pipeline-data-de.git
```

```
cd nyc-taxi-pipeline-data-de
```

---

### 2️⃣ Start Airflow using Docker

```
docker compose up airflow-init
docker compose up
```

---

### 3️⃣ Open Airflow UI

Open in browser:

```
http://localhost:8080
```

Default credentials:

```
username: airflow
password: airflow
```

---

### 4️⃣ Run the Pipeline

1. Enable the DAG:

```
nyc_taxi_pipeline
```

2. Click **Trigger DAG**

The pipeline will run automatically through all tasks.

---

# 📊 Output

After the pipeline runs successfully:

* Cleaned and transformed datasets will be generated
* Data will be loaded into MySQL tables:

  * `dim_time`
  * `dim_payment`
  * `fact_trips`
<img width="1919" height="988" alt="image (1)" src="https://github.com/user-attachments/assets/6c202163-bf2f-45c6-82ff-936e0da06b22" />
---
Dashboard.png
