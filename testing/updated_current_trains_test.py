from scripts.x_pipeline import *
from scripts.helper_functions import *

def test_enhanced_current_trains():
    """
    TEST FUNCTION - See what the enhanced current trains looks like
    """
    print("Testing enhanced current trains...")
    df = fetch_current_trains_enhanced()
    
    if not df.empty:
        print(f"Got {len(df)} current trains")
        print("Columns:", list(df.columns))
        print("\nSample data:")
        print(df[['TrainCode', 'delay_minutes', 'current_location', 'train_category']].head())
    else:
        print("No train data received")


test_enhanced_current_trains()