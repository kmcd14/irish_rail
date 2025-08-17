from scripts.x_pipeline import *
from scripts.helper_functions import *


def test_train_type_sampling():
    """
    TEST FUNCTION - See what train types we can discover
    """
    print("Testing train type sampling...")
    df = fetch_major_station_data_for_train_types()
    
    print(f"Discovered train types: {DISCOVERED_TRAIN_TYPES}")


test_train_type_sampling()