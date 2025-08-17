from scripts.x_pipeline import *
from scripts.helper_functions import *


def test_dart_stations():
    """
    TEST FUNCTION - See what DART stations we can get
    """
    print("Testing DART stations...")
    df = fetch_stations_with_dart_info()
    
    if not df.empty:
        print(f"Found {len(df)} DART stations")
        print(df[['StationDesc', 'StationCode', 'StationType']].head())
    else:
        print("No DART station data received")


test_dart_stations()