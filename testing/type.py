from scripts.train_types import *
from scripts.x_pipeline import *

def test_train_type_inference():
    """
    Test the train type inference on your current data
    """
    
    
    print("Testing train type inference...")
    
    # Test on current trains
    trains_df = fetch_current_trains_enhanced()
    if not trains_df.empty:
        trains_enhanced = add_train_types(trains_df)
        print(f"\nCurrent Trains ({len(trains_enhanced)} trains):")
        get_train_type_summary(trains_enhanced)
        
      
        cols = ['TrainCode', 'train_type', 'TrainOrigin', 'TrainDestination']
        available_cols = [col for col in cols if col in trains_enhanced.columns]
        print(trains_enhanced[available_cols].head(10))
    


    # Test on movements if available
    print("\n" + "="*50)
    movements_df = fetch_train_movements_enhanced()
    if not movements_df.empty:
        movements_enhanced = add_train_types(movements_df)
        print(f"\nTrain Movements ({len(movements_enhanced)} records):")
        get_train_type_summary(movements_enhanced)

