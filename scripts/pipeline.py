# Fetch, parse, and clean data from the Irish Rail API
from fetch_api import fetch_from_api
import time
import pandas as pd
from datetime import datetime
from parse import parse_xml_to_df
from cleaning import remove_linebreaks, remove_whitespace, object_to_date, object_to_float, object_tostring, object_to_time
from results_mapping import URL_CURRENT_TRAINS, FIELD_MAP_CURRENT_TRAINS, FIELD_MAP_STATION_INFO, URL_STATION_INFO, URL_TRAIN_MOVEMENTS, FIELD_MAP_TRAIN_MOVEMENTS

def fetch_current_trains():
    """
    Fetch current train data from the Irish Rail API.
    Returns a DataFrame with cleaned train data.
    """
    # Step 1: Fetch and parse data
    xml = fetch_from_api(URL_CURRENT_TRAINS)
    df = parse_xml_to_df(xml, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)

    # Step 2: Clean data
    df = object_tostring(df, ['train_code', 'direction', 'status', 'message'])
    df = object_to_float(df, ['latitude', 'longitude'])
    df = remove_linebreaks(df, ['message'])
    df = remove_whitespace(df, ['train_code', 'direction', 'message', 'status'])
    df = object_to_date(df, ['date'])

    #print(df.head())
    #print(df.info())

    return df


def fetch_station_info():
    """
    Fetch station information from the Irish Rail API.
    Returns a DataFrame with cleaned station data.
    """
    # Step 1: Fetch and parse data
    xml = fetch_from_api(URL_STATION_INFO)
    df = parse_xml_to_df(xml, 'objStation', FIELD_MAP_STATION_INFO)

    # Step 2: Clean data
    df = object_tostring(df, ['station_desc', 'station_code', 'alias', 'station_id'])
    df = object_to_float(df, ['latitude', 'longitude'])
    df = remove_whitespace(df, ['station_desc', 'station_code', 'alias'])

    print(df.head())
    print(df.info())

    return df



# get train mocements data
def fetch_train_movements():
    """
    Fetch train movements data for one train.
    Returns a DataFrame with cleaned train movements data.
    """
    trains_df = fetch_current_trains()
    all_movements = []

    for row in trains_df.itertuples():
        train_code, train_date = row.train_code, row.date
        url = URL_TRAIN_MOVEMENTS + f"?TrainId={train_code}&TrainDate={train_date.strftime('%d %b %Y')}"

        try:
            xml = fetch_from_api(url)
            df = parse_xml_to_df(xml, 'objTrainMovements', FIELD_MAP_TRAIN_MOVEMENTS)

            df = object_tostring(df, ['train_code', 'location_code', 'LocationFullName', 'TrainOrgin', 'TrainDestination', 'StopType'])
            df = remove_whitespace(df, ['train_code', 'location_code', 'LocationFullName', 'TrainOrgin', 'TrainDestination', 'StopType'])
            df = object_to_date(df, ['train_date'])
            df = object_to_time(df, ['ScheduledArrival', 'ScheduledDeparture', 'Arrival (actual)', 'Departure (actual)'])

            all_movements.append(df)

        except Exception as e:
            print(f"Error fetching movements for {train_code}: {e}")
            time.sleep(1)

    if all_movements:
        full_df = pd.concat(all_movements, ignore_index=True)
       #print(full_df.info())
       #print(full_df.head())
        return full_df


  


#fetch_station_info()
fetch_train_movements()


