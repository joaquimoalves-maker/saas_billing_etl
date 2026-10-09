# SaaS Billing & Subscription Event ETL Pipeline

An end-to-end, high-performance data engineering pipeline designed to ingest, transform, and load synthetic SaaS subscription lifecycle events into Google BigQuery using Python and Polars.

## Architecture & Workflow

[ Data Generator ] ---> ( Raw NDJSON ) ---> [ Polars ETL Engine ] ---> ( Parquet ) ---> [ BigQuery Warehouse ]


1. **Ingestion & Data Generation (`generate_data.py`)**: Simulates 5,000 raw subscription billing events (MRR, churn, upgrades, plan changes) exported in NDJSON format.
2. **Transformation Engine (`etl_transform.py`)**: Uses **Polars** for high-throughput memory-efficient parsing, enforcing UTC datetime types, extracting calendar partitions (`event_date`, `event_year`, `event_month`), and filtering invalid records.
3. **Storage & Serialization**: Saves clean records into compressed Snappy Parquet format for optimized cloud upload speed and reduced storage overhead.
4. **Data Warehouse Loading (`load_to_bigquery.py`)**: Programmatically loads Parquet batches into Google BigQuery using GCP Service Account authentication (`WRITE_TRUNCATE` pattern).

---

## Tech Stack

* **Language**: Python 3.14
* **Data Processing**: Polars (Lazy/Eager DataFrames)
* **Cloud Warehouse**: Google BigQuery
* **Data Serialization**: Apache Parquet (Snappy compression)
* **Synthetic Data**: Faker

---

## Data Schema & Analytical Query Sample

### Data Schema (`saas_analytics.raw_saas_events`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `event_id` | STRING | Unique event identifier |
| `timestamp` | TIMESTAMP | Event execution time (UTC) |
| `customer_id` | STRING | Account reference |
| `event_type` | STRING | Subscription status change event |
| `plan_id` | STRING | Active tier (`starter_tier`, `pro_tier`, `enterprise_tier`) |
| `mrr_amount` | FLOAT | Monthly Recurring Revenue contribution |
| `payment_status`| STRING | `succeeded` or `failed` |
| `event_date` | DATE | Derived partitioning date |

### Sample Metric Query

```sql
SELECT 
    event_type, 
    COUNT(*) AS total_events, 
    ROUND(SUM(mrr_amount), 2) AS total_mrr
FROM `saas-billing-etl.saas_analytics.raw_saas_events`
GROUP BY 1
ORDER BY total_mrr DESC;

Local Setup & Execution
Prerequisites

    Python 3.10+

    Google Cloud Platform Project with BigQuery API enabled

    GCP Service Account Key (gcp_key.json) with BigQuery Admin role

Instructions

    Clone Repository & Setup Environment:
    Bash

    git clone [https://github.com/joaquimoalves-maker/saas_billing_etl.git](https://github.com/joaquimoalves-maker/saas_billing_etl.git)
    cd saas_billing_etl
    python -m venv venv
    source venv/bin/activate
    pip install polars google-cloud-bigquery faker pyarrow

    Configure GCP Credentials:
    Bash

    export GOOGLE_APPLICATION_CREDENTIALS="gcp_key.json"

    Run Pipeline:
    Bash

    python generate_data.py
    python etl_transform.py
    python load_to_bigquery.py
