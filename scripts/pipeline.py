# pipeline.py

import pandas as pd
import logging
from datetime import datetime
import time

from .fetch_api import fetch_from_api
from .parse import parse_xml_to_df
from .cleaning import *
from .results_mapping import *
from .helper_functions import *
from .train_types import *
from .insert import * 

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



### EXTRACT - Get data from API ###


# get stations
def extract_stations():
    """Extract station data from API"""
    try:
        logger.info("Extracting station data...")
        xml = fetch_from_api(URL_STATION_INFO)
        df = parse_xml_to_df(xml, 'objStation', FIELD_MAP_STATION_INFO)
        logger.info(f"Extracted {len(df)} stations")
        return df
    except Exception as e:
        logger.error(f"Failed to extract stations: {e}")
        return pd.DataFrame()

# get current trains
def extract_current_trains():
    """Extract current trains data from API"""
    try:
        logger.info("Extracting current trains...")
        xml = fetch_from_api(URL_CURRENT_TRAINS)
        df = parse_xml_to_df(xml, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)
        logger.info(f"Extracted {len(df)} current trains")
        return df
    except Exception as e:
        logger.error(f"Failed to extract current trains: {e}")
        return pd.DataFrame()


# get train movements
def extract_train_movements():
    """Extract train movements for all current trains"""
    try:
        logger.info("Extracting train movements...")
        
        # First get current trains to know which movements to fetch
        trains_df = extract_current_trains()
        if trains_df.empty:
            return pd.DataFrame()
        
        all_movements = []
        
        for row in trains_df.itertuples():
            train_code = row.TrainCode
            train_date = row.TrainDate
            
            try:
                # Handle case where TrainDate is a string or datetime
                if isinstance(train_date, str):
                    # If it's already a string, use it directly
                    formatted_date = train_date
                else:
                    # If it's a datetime, format it
                    formatted_date = train_date.strftime('%d %b %Y')
                
                url = URL_TRAIN_MOVEMENTS + f"?TrainId={train_code}&TrainDate={formatted_date}"
                xml = fetch_from_api(url)
                df = parse_xml_to_df(xml, 'objTrainMovements', FIELD_MAP_TRAIN_MOVEMENTS)
                
                if not df.empty:
                    df['fetched_at'] = pd.Timestamp.now()
                    all_movements.append(df)
                
                time.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Failed to get movements for {train_code}: {e}")
                continue
        
        if all_movements:
            combined_df = pd.concat(all_movements, ignore_index=True)
            logger.info(f"Extracted {len(combined_df)} train movement records")
            return combined_df
        
        return pd.DataFrame()
        
    except Exception as e:
        logger.error(f"Failed to extract train movements: {e}")
        return pd.DataFrame()




### TRANSFORM - Clean and transform data ###

# clean station data
def transform_stations(df):
    """Transform station data"""
    if df.empty:
        return df
    
    logger.info("Transforming station data...")
    
    # Clean and standardise station fields
    df = object_tostring(df, ['StationDesc', 'StationCode', 'StationAlias', 'StationId', 'StationType'])
    df = object_to_float(df, ['StationLatitude', 'StationLongitude'])
    df = remove_whitespace(df, ['StationDesc', 'StationCode', 'StationAlias', 'StationType'])
    
    # Add timestamp
    df['updated_at'] = pd.Timestamp.now()
    
    return df


# Clean current trains
def transform_current_trains(df):
    """Transform current trains data"""
    if df.empty:
        return df
    
    logger.info("Transforming current trains data...")
    
    # Apply your existing cleaning functions
    df = object_tostring(df, ['TrainCode', 'Direction', 'TrainStatus', 'PublicMessage', 'TrainType'])
    df = object_to_float(df, ['TrainLatitude', 'TrainLongitude'])
    df = remove_linebreaks(df, ['PublicMessage'])
    df = remove_whitespace(df, ['TrainCode', 'Direction', 'PublicMessage', 'TrainStatus', 'TrainType'])
    df = object_to_date(df, ['TrainDate'])
    
    # Add extra fields
    df = add_extra_fields(df)
    df = add_train_types(df)
    
    # Add collection timestamp
    df['collected_at'] = pd.Timestamp.now()
    
    logger.info(f"Enhanced {len(df)} current trains with delay/type information")
    return df


# clean train movements
def transform_train_movements(df):
    """Transform train movements data"""
    if df.empty:
        return df
    
    logger.info("Transforming train movements data...")
    
    # Clean fields
    df = object_tostring(df, ['TrainCode', 'LocationCode', 'LocationFullName','TrainOrigin', 'TrainDestination', 'StopType'])
    df = remove_whitespace(df, ['TrainCode', 'LocationCode', 'LocationFullName','TrainOrigin', 'TrainDestination', 'StopType'])
    df = object_to_date(df, ['TrainDate'])
    df = object_to_time(df, ['ScheduledArrival', 'ScheduledDeparture','arrival_actual', 'departure_actual'])
    
    # Add extra columns
    df = add_extra_fields(df)
    df = add_train_types(df)
    
    logger.info(f"Enhanced {len(df)} train movement records")
    return df




### LOAD - Insert into database ###

# Insert stations into DB
def load_stations(df):
    """Load stations into database"""
    if df.empty:
        return
    
    try:
        insert_data(df, 'stations')
        logger.info(f"Loaded {len(df)} stations to database")
    except Exception as e:
        logger.error(f"Failed to load stations: {e}")


# Insert current trains into DB
def load_current_trains(df):
    """Load current trains into database"""
    if df.empty:
        return
    
    try:
        insert_data(df, 'current_trains')
        logger.info(f"Loaded {len(df)} current trains to database")
    except Exception as e:
        logger.error(f"Failed to load current trains: {e}")


# insert train movements into DB
def load_train_movements(df):
    """Load train movements into database"""
    if df.empty:
        return
    
    try:
        insert_data(df, 'train_movements')
        logger.info(f"Loaded {len(df)} train movements to database")
    except Exception as e:
        logger.error(f"Failed to load train movements: {e}")


def run_stations_etl():
    df = extract_stations()
    df = transform_stations(df)
    load_stations(df)


def run_current_trains_etl():
    df = extract_current_trains()
    df = transform_current_trains(df)
    load_current_trains(df)


def run_train_movements_etl():
    df = extract_train_movements()
    df = transform_train_movements(df)
    load_train_movements(df)