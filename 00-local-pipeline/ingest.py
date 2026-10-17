import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine, text
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
load_dotenv(override=True)


def get_env(key: str):
    """
    Get the variable from the .env file. All variables are required
    If not valid variable raise error
    """
    val = os.getenv(key)

    if val is None:
        raise EnvironmentError(f"Missing required env {key}")

    return val


DATABASE_URL = get_env("DATABASE_URL")
TAXI_FILE = get_env("TAXI_FILE")
TABLE = "yellow_taxi_data"


def main():
    engine = create_engine(url=DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE {TABLE};"))
        conn.commit()
        logging.info(f"Table {TABLE} dropped")

    pq_taxi_data = pq.ParquetFile(TAXI_FILE)
    total_rows = pq_taxi_data.metadata.num_rows
    logging.info(f"Total rows: {total_rows}")

    inserted_rows = 0
    for batch in pq_taxi_data.iter_batches(batch_size=10000):
        df = pa.Table.from_batches([batch]).to_pandas()
        df.to_sql(
            con=engine,
            name=TABLE,
            if_exists="append",
            index=False,
        )

        inserted_rows += batch.num_rows
        logging.info(f"Inserted rows {inserted_rows} / {total_rows}")


if __name__ == "__main__":
    main()
