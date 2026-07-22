import dlt
import pandas as pd
from pathlib import Path

# Path to your generated CSVs
DATA_DIR = Path(__file__).parent.parent / "data_generation"

# Define the CSVs to load and their table names
SOURCES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_line_items": "order_line_items.csv",
    "reviews": "reviews.csv",
    "date_dimension": "date_dimension.csv",
}

def load_csv(table_name: str, file_name: str):
    """Read a CSV and yield rows as dicts for dlt to ingest."""
    file_path = DATA_DIR / file_name
    df = pd.read_csv(file_path)
    print(f"Loading {len(df)} rows into {table_name}...")
    for row in df.to_dict(orient="records"):
        yield row

def run_pipeline():
    # Initialize dlt pipeline
    # destination: duckdb file path
    # dataset_name: the schema name in DuckDB (raw)
    pipeline = dlt.pipeline(
        pipeline_name="retail_ingestion",
        destination=dlt.destinations.duckdb(
            "/Users/shlok/Projects/retail-analytics-engineering/warehouse.duckdb"
        ),
        dataset_name="raw",
    )

    # Load each CSV as a separate resource
    resources = []
    for table_name, file_name in SOURCES.items():
        resource = dlt.resource(
            load_csv(table_name, file_name),
            name=table_name,
            write_disposition="replace",  # replace on every run — idempotent
        )
        resources.append(resource)

    # Run all resources in one pipeline execution
    load_info = pipeline.run(resources)
    print(load_info)

if __name__ == "__main__":
    run_pipeline()