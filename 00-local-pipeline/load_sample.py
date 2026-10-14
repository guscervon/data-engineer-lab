import os
import pandas as pd
from sqlalchemy import create_engine, over
from dotenv import load_dotenv


load_dotenv(override=True)
DB_URL = os.getenv("DATABASE_URL")


def main():
    engine = create_engine(DB_URL)

    df = pd.read_parquet("data/yellow_tripdata_2026-08.parquet")

    df.head(100).to_sql(name="yellow_taxi_data", con=engine, if_exists="fail")


if __name__ == "__main__":
    main()
