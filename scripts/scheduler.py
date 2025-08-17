import schedule
import time
import logging
from pipeline import (run_current_trains_etl,run_train_movements_etl,run_stations_etl)


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("irish_rail_etl.log"),
        logging.StreamHandler()  # Also prints to console
    ]
)


# run ETL with logging
def run_etl_with_logging(etl_func, etl_name):
    """Run an ETL function with error handling and logging."""
    try:
        logging.info(f"Starting {etl_name} ETL...")
        etl_func()
        logging.info(f"{etl_name} ETL completed successfully.")
    except Exception as e:
        logging.error(f"{etl_name} ETL failed: {e}")


# Scheduler setup
def start_scheduled_collection():
    # Run all ETLs once at startup
    run_etl_with_logging(run_current_trains_etl, "Current Trains")
    run_etl_with_logging(run_train_movements_etl, "Train Movements")
    run_etl_with_logging(run_stations_etl, "Stations")

    # Schedule ETLs
    schedule.every(5).minutes.do(run_etl_with_logging, run_current_trains_etl, "Current Trains")
    schedule.every(15).minutes.do(run_etl_with_logging, run_train_movements_etl, "Train Movements")
    schedule.every().day.at("02:00").do(run_etl_with_logging, run_stations_etl, "Stations")

    logging.info("Scheduler started. Waiting for jobs...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error in scheduler loop: {e}")
            time.sleep(60)  # Wait before retrying


if __name__ == "__main__":
    start_scheduled_collection()
