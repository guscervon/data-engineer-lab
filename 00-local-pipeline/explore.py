import pyarrow.parquet as pq
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
FILE = "data/yellow_tripdata_2026-08.parquet"


def main():
    metadata = pq.read_metadata(FILE)
    logging.info(f"Metada {FILE}:\n{metadata}")

    schema = pq.read_schema(FILE)
    column_names = schema.names
    logging.info(f"column names from {FILE}:\n{column_names}")


if __name__ == "__main__":
    main()
