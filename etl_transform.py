import polars as pl

def run_etl():
    df_raw = pl.read_ndjson("raw_saas_events.json")

    df_transformed = (
        df_raw
        .with_columns(
            pl.col("timestamp").str.to_datetime(time_zone="UTC")
        )
        .with_columns([
            pl.col("timestamp").dt.date().alias("event_date"),
            pl.col("timestamp").dt.year().alias("event_year"),
            pl.col("timestamp").dt.month().alias("event_month")
        ])
        .filter(pl.col("mrr_amount") >= 0.0)
        .sort("timestamp")
    )

    df_transformed.write_parquet(
        "processed_saas_events.parquet",
        compression="snappy"
    )

if __name__ == "__main__":
    run_etl()
