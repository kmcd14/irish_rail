# Fetch, parse, and clean data from the Irish Rail API

from .fetch_api import fetch_from_api
from .parse import parse_xml_to_df
from .cleaning import *
from .results_mapping import *
import pandas as pd
import time

def fetch_current_trains():
    """
    Fetch current train data from the Irish Rail API.
    Returns a DataFrame with cleaned train data.
    """
    xml = fetch_from_api(URL_CURRENT_TRAINS)
    df = parse_xml_to_df(xml, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)

    df = object_tostring(df, ['TrainCode', 'Direction', 'TrainStatus', 'PublicMessage'])
    df = object_to_float(df, ['TrainLatitude', 'TrainLongitude'])
    df = remove_linebreaks(df, ['PublicMessage'])
    df = remove_whitespace(df, ['TrainCode', 'Direction', 'PublicMessage', 'TrainStatus'])
    df = object_to_date(df, ['TrainDate'])

    return df


def fetch_station_info():
    """
    Fetch station information from the Irish Rail API.
    Returns a DataFrame with cleaned station data.
    """
    xml = fetch_from_api(URL_STATION_INFO)
    df = parse_xml_to_df(xml, 'objStation', FIELD_MAP_STATION_INFO)

    df = object_tostring(df, ['StationDesc', 'StationCode', 'StationAlias', 'StationId', 'StationType'])
    df = object_to_float(df, ['StationLatitude', 'StationLongitude'])
    df = remove_whitespace(df, ['StationDesc', 'StationCode', 'StationAlias', 'StationType'])

    #print(df.info())
    return df


def fetch_train_movements():
    """
    Fetch train movements data for all current trains.
    Returns a DataFrame with cleaned train movements data.
    """
    trains_df = fetch_current_trains()
    fetch_current_train_types()
    all_movements = []

    for row in trains_df.itertuples():
        train_code = row.TrainCode
        train_date = row.TrainDate
        url = URL_TRAIN_MOVEMENTS + f"?TrainId={train_code}&TrainDate={train_date.strftime('%d %b %Y')}"

        try:
            xml = fetch_from_api(url)
            df = parse_xml_to_df(xml, 'objTrainMovements', FIELD_MAP_TRAIN_MOVEMENTS)

            df = object_tostring(df, ['TrainCode', 'LocationCode', 'LocationFullName','TrainOrigin', 'TrainDestination', 'StopType'])
            df = remove_whitespace(df, ['TrainCode', 'LocationCode', 'LocationFullName','TrainOrigin', 'TrainDestination', 'StopType'])
            df = object_to_date(df, ['TrainDate'])
            df = object_to_time(df, ['ScheduledArrival', 'ScheduledDeparture','arrival_actual', 'departure_actual'])


            df['fetched_at'] = pd.Timestamp.now()

            all_movements.append(df)

        except Exception as e:
            print(f"Error fetching movements for {train_code}: {e}")
            time.sleep(1)

    if all_movements:
        return pd.concat(all_movements, ignore_index=True)


# Train type cache
_train_type_cache = {}

def fetch_current_train_types():
    """
    Fetch all current trains and build a mapping of TrainCode -> TrainType.
    """
    global _train_type_cache
    try:
        root = fetch_from_api(URL_CURRENT_TRAINS)
        df = parse_xml_to_df(root, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)

        df = object_tostring(df, ['TrainCode', 'TrainType'])
        df = remove_whitespace(df, ['TrainCode', 'TrainType'])
        _train_type_cache = pd.Series(df.TrainType.values, index=df.TrainCode).to_dict()

    except Exception as e:
        print(f"Error fetching current train types: {e}")
        _train_type_cache = {}
