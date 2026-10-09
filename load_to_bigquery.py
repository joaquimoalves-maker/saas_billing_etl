import os
from google.cloud import bigquery

def load_parquet():
    client = bigquery.Client()

    project_id = client.project
    dataset_id = f"{project_id}.saas_analytics"
    table_id = f"{dataset_id}.raw_saas_events"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    file_path = "processed_saas_events.parquet"

    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_id}.")

if __name__ == "__main__":
    load_parquet()
