# scripts/helper_functions.py 
# Helper functions for data processing and enhancement
import pandas as pd
import re
from datetime import datetime

def extract_delay_from_message(message):
    """
    Extract delay minutes from PublicMessage
    Example: "A105 08:00 - Belfast to Dublin (5 mins late)" -> 5
    """
    if pd.isna(message) or message == "":
        return 0
    
    # Look for pattern like "(5 mins late)" or "(-3 mins late)"
    delay_pattern = r'\(([+-]?\d+) mins late\)'
    match = re.search(delay_pattern, str(message))
    
    if match:
        return int(match.group(1))
    
    # If no delay found, assume on time
    return 0

def extract_current_location(message):
    """
    Extract current location from PublicMessage
    Example: "Arrived Dundalk next stop Newry" -> "Dundalk"
    """
    if pd.isna(message) or message == "":
        return None
    
    message_str = str(message)
    
    # Look for "Departed X next stop Y"
    departed_pattern = r'Departed ([^n]+) next stop'
    departed_match = re.search(departed_pattern, message_str)
    if departed_match:
        return departed_match.group(1).strip()
    
    # Look for "Arrived X next stop Y" or "Arrived X"
    arrived_pattern = r'Arrived ([^n]+?)(?:\s+next stop|$)'
    arrived_match = re.search(arrived_pattern, message_str)
    if arrived_match:
        return arrived_match.group(1).strip()
    
    return None

def get_train_category(train_code):
    """
    Get train category from train code
    A = Intercity, D = DART, P = Freight, etc.
    """
    if pd.isna(train_code) or train_code == "":
        return "N/A"
    
    return str(train_code)[0] if len(str(train_code)) > 0 else "N/A"

def classify_route(origin, destination):
    """
    Classify route type based on origin and destination
    """
    if pd.isna(origin) or pd.isna(destination):
        return "Unknown"
    
    origin_str = str(origin).upper()
    destination_str = str(destination).upper()
    
    # Dublin area services
    dublin_keywords = ['DUBLIN', 'CONNOLLY', 'HEUSTON', 'PEARSE']
    has_dublin_origin = any(keyword in origin_str for keyword in dublin_keywords)
    has_dublin_dest = any(keyword in destination_str for keyword in dublin_keywords)
    
    if has_dublin_origin or has_dublin_dest:
        # Check if it's intercity (Dublin to major city)
        major_cities = ['CORK', 'GALWAY', 'LIMERICK', 'WATERFORD', 'BELFAST', 'SLIGO']
        has_major_city = any(city in origin_str or city in destination_str for city in major_cities)
        
        if has_major_city:
            return "Intercity"
        else:
            return "Dublin_Commuter"
    
    # Non-Dublin routes
    return "Regional"

def add_extra_fields(df):
    """
    Add enhanced fields to any dataframe with train data
    """
    if df.empty:
        return df
    
    # Make a copy to not modify  original
    updated_df= df.copy()
    
    # Add delay information if it exists
    if 'PublicMessage' in updated_df.columns:
       updated_df['delay_minutes'] =updated_df['PublicMessage'].apply(extract_delay_from_message)
       updated_df['current_location'] =updated_df['PublicMessage'].apply(extract_current_location)
    
    # Add train category if TrainCode exists
    if 'TrainCode' in updated_df.columns:
       updated_df['train_category'] =updated_df['TrainCode'].apply(get_train_category)
    
    # Add route classification if origin/destination exists
    if 'TrainOrigin' in updated_df.columns and 'TrainDestination' in updated_df.columns:
       updated_df['route_classification'] =updated_df.apply(
            lambda row: classify_route(row['TrainOrigin'], row['TrainDestination']), axis=1
        )
    
    # Add collection timestamp
    updated_df['enhanced_at'] = pd.Timestamp.now()
    
    return updated_df

# Dictionary to store train types we discover
DISCOVERED_TRAIN_TYPES = {}

def update_train_type_cache(df):
    """
    Update our cache of train types from any dataframe that has TrainCode and TrainType
    """
    global DISCOVERED_TRAIN_TYPES
    
    if df.empty or 'TrainCode' not in df.columns or 'TrainType' not in df.columns:
        return
    
    # Get non-empty train types
    valid_types = df[df['TrainType'].notna() & (df['TrainType'] != '')][['TrainCode', 'TrainType']]
    
    # Update our cache
    for _, row in valid_types.iterrows():
        DISCOVERED_TRAIN_TYPES[row['TrainCode']] = row['TrainType']
    
    print(f"Updated train type cache. Now have {len(DISCOVERED_TRAIN_TYPES)} train types")


def enrich_with_cached_train_types(df):
    """
    Add train types from our cache to any dataframe with TrainCode
    """
    if df.empty or 'TrainCode' not in df.columns:
        return df
    
    updated_df= df.copy()
    
    # Add cached train type if we don't already have it
    if 'TrainType' not in updated_df.columns:
       updated_df['TrainType'] =updated_df['TrainCode'].map(DISCOVERED_TRAIN_TYPES)
    else:
        # Fill empty train types with cached ones
       updated_df['TrainType'] =updated_df['TrainType'].fillna(
           updated_df['TrainCode'].map(DISCOVERED_TRAIN_TYPES)
        )
    
    return updated_df