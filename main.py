# main.py
# Test script for Irish Rail data extraction, transformation, and loading

import logging
from datetime import datetime

# Import functions from completepipeline.py
from scripts.pipeline import (
    extract_stations,
    extract_current_trains,
    extract_train_movements,
    transform_stations,
    transform_current_trains,
    transform_train_movements,
    load_stations,
    load_current_trains,
    load_train_movements
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to test the data extraction, transformation, and loading process.
    This function extracts data from the Irish Rail API, transforms it,
    and loads it into a database.
    """
    logger.info("Starting Irish Rail data ETL process")
    start_time = datetime.now()
    
    # Dictionary to store results
    results = {}
    
    # Process stations data
    logger.info("Processing stations data")
    raw_stations = extract_stations()
    if not raw_stations.empty:
        clean_stations = transform_stations(raw_stations)
        results['stations'] = clean_stations
        logger.info(f"Extracted and transformed {len(clean_stations)} stations")
        # Print sample of stations data
        logger.info("Sample of stations data:")
        print(clean_stations.head(3))
        print("\n")
        
        # Load stations data into database
        load_stations(clean_stations)
    else:
        logger.warning("No stations data extracted")
    
    # Process current trains data
    logger.info("Processing current trains data")
    raw_current_trains = extract_current_trains()
    if not raw_current_trains.empty:
        clean_current_trains = transform_current_trains(raw_current_trains)
        results['current_trains'] = clean_current_trains
        logger.info(f"Extracted and transformed {len(clean_current_trains)} current trains")
        # Print sample of current trains data
        logger.info("Sample of current trains data:")
        print(clean_current_trains.head(3))
        print("\n")
        
        # Print information about the new columns
        if 'delay_minutes' in clean_current_trains.columns:
            delayed_trains = clean_current_trains[clean_current_trains['delay_minutes'] > 0]
            logger.info(f"Number of delayed trains: {len(delayed_trains)}")
            if not delayed_trains.empty:
                logger.info(f"Average delay: {delayed_trains['delay_minutes'].mean():.1f} minutes")
        
        if 'train_category' in clean_current_trains.columns:
            logger.info("Train categories:")
            print(clean_current_trains['train_category'].value_counts())
            print("\n")
        
        # Load current trains data into database
        load_current_trains(clean_current_trains)
    else:
        logger.warning("No current trains data extracted")
    
    # Process train movements data
    logger.info("Processing train movements data")
    raw_train_movements = extract_train_movements()
    if not raw_train_movements.empty:
        clean_train_movements = transform_train_movements(raw_train_movements)
        results['train_movements'] = clean_train_movements
        logger.info(f"Extracted and transformed {len(clean_train_movements)} train movements")
        # Print sample of train movements data
        logger.info("Sample of train movements data:")
        print(clean_train_movements.head(3))
        print("\n")
        
        # Print information about the new columns
        if 'route_classification' in clean_train_movements.columns:
            logger.info("Route classifications:")
            print(clean_train_movements['route_classification'].value_counts())
            print("\n")
        
        # Load train movements data into database
        load_train_movements(clean_train_movements)
    else:
        logger.warning("No train movements data extracted")
    
    # Log summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"ETL process completed in {duration:.1f} seconds")
    
    # Print overall summary
    logger.info("Summary of processed data:")
    for data_type, data in results.items():
        if not data.empty:
            logger.info(f"  {data_type}: {len(data)} records")
            logger.info(f"  {data_type} columns: {list(data.columns)}")
        else:
            logger.info(f"  {data_type}: No data")
    
    return results

if __name__ == "__main__":
    main()