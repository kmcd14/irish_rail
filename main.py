# main.py

from scripts.fetch_api import fetch_from_api
from scripts.parse import parse_xml_to_df
from scripts.config import URL_CURRENT_TRAINS, FIELD_MAP_CURRENT_TRAINS
from scripts.config import URL_STATION_INFO, FIELD_MAP_STATION_INFO 
from scripts.config import URL_TRAIN_MOVEMENTS, FIELD_MAP_TRAIN_MOVEMENTS
from scripts.config import URL_STATION_DATA_BY_CODE_WITH_MINUTES, FIELD_MAP_STATION_DATA_BY_CODE_WITH_MINUTES

# Fetch current trains data from the API
root = fetch_from_api(URL_CURRENT_TRAINS)
current_trains_df = parse_xml_to_df(root, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)
print(current_trains_df.head())

# Fetch station information from the API
root_station = fetch_from_api(URL_STATION_INFO)
station_info_df = parse_xml_to_df(root_station, 'objStation', FIELD_MAP_STATION_INFO)
print(station_info_df.head())

