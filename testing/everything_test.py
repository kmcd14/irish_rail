from scripts.x_pipeline import *
from scripts.helper_functions import *


def collect_all_data_once():
    """
    SIMPLE FUNCTION - Collect all data once (not scheduled)
    Use this to test everything works
    """
    print("=" * 50)
    print("Starting data collection...")
    
    # Your existing functions
    print("\n1. Fetching current trains...")
    current_trains = fetch_current_trains_enhanced()
    
    print("\n2. Fetching stations...")
    stations = fetch_station_info()
    
    print("\n3. Fetching DART stations...")
    dart_stations = fetch_stations_with_dart_info()
    
    print("\n4. Sampling for train types...")
    sample_data = fetch_major_station_data_for_train_types()
    
    print("\n5. Fetching train movements...")
    movements = fetch_train_movements_enhanced()
    
    print("=" * 50)
    print("Collection complete!")
    
    return {
        'current_trains': current_trains,
        'stations': stations,
        'dart_stations': dart_stations,
        'sample_data': sample_data,
        'movements': movements
    }


collect_all_data_once()