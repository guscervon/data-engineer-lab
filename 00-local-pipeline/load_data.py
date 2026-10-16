import os
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
load_dotenv(override=True)

DB_URL = os.getenv("DATABASE_URL")
TAXI_DATA = os.getenv("TAXI_FILE")


def main():
    taxi_data = pq.ParquetFile(TAXI_DATA)
    total = taxi_data.metadata.num_rows()
    logging.info(f"Total rows in parquet file: {total}")

    engine = create_engine(url=DB_URL)
    loaded_count = 0
    for batch in taxi_data.iter_batches(batch_size=10000):
        batch_table = pa.Table.from_batches([batch]).to_pandas()
        if loaded_count == 0:
            batch_table.to_sql(
                name="yellow_taxi_data",
                con=engine,
                if_exists="replace",
                index=False,
                method="multi",
            )
        else:
            batch_table.to_sql(
                name="yellow_taxi_data",
                con=engine,
                if_exists="append",
                index=False,
                method="multi",
            )
        loaded_count += batch.num_rows
        logging.info(f"{loaded_count} / {total}")


if __name__ == "__main__":
    main()
