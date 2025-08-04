# Fetch, parse, and clean data from the Irish Rail API
from fetch_api import fetch_from_api
from parse import parse_xml_to_df
from cleaning import remove_linebreaks, remove_whitespace, object_to_date, object_to_float, object_tostring
from results_mapping import URL_CURRENT_TRAINS, FIELD_MAP_CURRENT_TRAINS


# Step 1: Fetch and parse data
root = fetch_from_api(URL_CURRENT_TRAINS)
df = parse_xml_to_df(root, 'objTrainPositions', FIELD_MAP_CURRENT_TRAINS)

# Step 2: Clean data
df = object_tostring(df, ['train_code', 'direction', 'status', 'message'])
df = object_to_float(df, ['latitude', 'longitude'])
df = remove_linebreaks(df, ['message'])
df = remove_whitespace(df, ['train_code', 'direction', 'message', 'status'])
df = object_to_date(df, ['date'])


print(df.head())
print(df.info())

    

