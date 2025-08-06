from scripts.fetch_api import fetch_from_api
from scripts.parse import parse_xml_to_df
from scripts.results_mapping import URL_CURRENT_TRAINS, FIELD_MAP_CURRENT_TRAINS
from scripts.results_mapping import URL_TRAIN_MOVEMENTS, FIELD_MAP_TRAIN_MOVEMENTS


from datetime import datetime
import time

# Fetch current trains data from the API
root = fetch_from_api(URL_CURRENT_TRAINS)
current_trains_df = parse_xml_to_df(root, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)
#print(current_trains_df.head())


# Test movement of one train
for row in current_trains_df.head(1).itertuples():
    train_code, train_date  = row.train_code, row.date
    #print(train_date, train_code)

    url = URL_TRAIN_MOVEMENTS + f"?TrainId={train_code}&TrainDate={train_date}"
    try:
        root = fetch_from_api(url)
        movement_df = parse_xml_to_df(root, 'objTrainMovements', FIELD_MAP_TRAIN_MOVEMENTS)
        print(f'Train movements for {train_code} on {train_date}:')
        print(movement_df.head())
    except Exception as e:
        print(f"Error fetching train movements for {train_code} on {train_date}: {e}")

        time.sleep(1)  # Sleep to avoid hitting API rate limits