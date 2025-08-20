# scripts\schedule.py - Single run version for GitHub Actions/cron
import os
import sys
import logging
from datetime import datetime
from pipeline import (run_current_trains_etl, run_train_movements_etl, run_stations_etl)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Only console for GitHub Actions
)

def run_etl_based_on_schedule():
    """Determine which ETL to run based on current time"""
    now = datetime.now()
    minute = now.minute
    hour = now.hour
    
    # Determine which ETL to run based on schedule
    if hour == 2 and minute == 0:
        # Daily stations update at 2 AM
        run_etl_with_logging(run_stations_etl, "Stations")
    elif minute % 15 == 0:
        # Every 15 minutes: run train movements
        run_etl_with_logging(run_train_movements_etl, "Train Movements")
    elif minute % 5 == 0:
        # Every 5 minutes: run current trains
        run_etl_with_logging(run_current_trains_etl, "Current Trains")
    else:
        logging.info(f"No ETL scheduled for {now.strftime('%H:%M')} - skipping")

def run_etl_with_logging(etl_func, etl_name):
    """Run an ETL function with error handling and logging."""
    try:
        logging.info(f"Starting {etl_name} ETL...")
        result = etl_func()
        logging.info(f"{etl_name} ETL completed successfully.")
        return result
    except Exception as e:
        logging.error(f"{etl_name} ETL failed: {e}", exc_info=True)
        sys.exit(1)  # Fail the job if ETL fails

def run_specific_etl():
    """Run specific ETL based on command line argument"""
    if len(sys.argv) > 1:
        etl_type = sys.argv[1].lower()
        
        if etl_type == 'trains':
            run_etl_with_logging(run_current_trains_etl, "Current Trains")
        elif etl_type == 'movements':
            run_etl_with_logging(run_train_movements_etl, "Train Movements")
        elif etl_type == 'stations':
            run_etl_with_logging(run_stations_etl, "Stations")
        elif etl_type == 'all':
            run_etl_with_logging(run_current_trains_etl, "Current Trains")
            run_etl_with_logging(run_train_movements_etl, "Train Movements")
            run_etl_with_logging(run_stations_etl, "Stations")
        else:
            logging.error(f"Unknown ETL type: {etl_type}")
            logging.info("Usage: python schedule.py [trains|movements|stations|all]")
            sys.exit(1)
    else:
        # No argument provided - run based on schedule
        run_etl_based_on_schedule()

if __name__ == "__main__":
    run_specific_etl()