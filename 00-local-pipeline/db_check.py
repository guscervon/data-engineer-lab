import os
import psycopg
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")


def main():
    # Open connection to the database
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        # Open cursor to perform database operations
        with conn.cursor() as cur:
            cur.execute("SELECT version();")

            logging.info(f"PostgreSQL version: {cur.fetchone()}")


if __name__ == "__main__":
    main()
