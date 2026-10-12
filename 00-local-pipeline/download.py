from urllib.request import urlretrieve
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

MONTH = "2026-08"
URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{MONTH}.parquet"
DIRECTORY_STORE = Path("data") / f"yellow_tripdata_{MONTH}.parquet"


def main():
    DIRECTORY_STORE.parent.mkdir(exist_ok=True)
    if not DIRECTORY_STORE.exists():
        urlretrieve(URL, DIRECTORY_STORE)
    logging.info(f"{DIRECTORY_STORE} ({DIRECTORY_STORE.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
