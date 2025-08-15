# train_types.py -  API doesn't give  train types, use logic to find them

import pandas as pd
import re


# Get train type from code
def train_type_from_code(train_code):
    """
    Gathers train type from the train code pattern
    NOTE: need to check routes too
    """
    if pd.isna(train_code) or train_code == "":
        return "Unknown"
    
    code = str(train_code).upper().strip()
    
    # DART services (Dublin Area Rapid Transit)
    if code.startswith('D'):
        return "DART"
    
    # Intercity services  
    if code.startswith('A'):
        return "Intercity"
    
    # Freight/Post services
    if code.startswith('P'):
        return "Freight"
    
    # E-codes could be Enterprise OR DART - need route info to determine
    if code.startswith('E'):
        return "E_Code_Unknown" 
    
    # Commuter services
    if code.startswith('C'):
        return "Commuter"
    
    # Mark and Lane (Special services)
    if code.startswith('M') or code.startswith('L'):
        return "Special"
    
    return "Unknown"



# Train type from route
def train_type_from_route(origin, destination):
    """
    Gather train type from route pattern
    """
    if pd.isna(origin) or pd.isna(destination):
        return "Unknown"
    
    origin_str = str(origin).upper()
    dest_str = str(destination).upper()
    
    # REAL Enterprise routes (only Belfast-Dublin intercity)
    belfast_keywords = ['BELFAST', 'CENTRAL']
    dublin_keywords = ['DUBLIN', 'CONNOLLY']
    
    origin_belfast = any(keyword in origin_str for keyword in belfast_keywords)
    dest_belfast = any(keyword in dest_str for keyword in belfast_keywords)
    origin_dublin = any(keyword in origin_str for keyword in dublin_keywords)
    dest_dublin = any(keyword in dest_str for keyword in dublin_keywords)
    
    # True Enterprise: Belfast <-> Dublin
    if (origin_belfast and dest_dublin) or (origin_dublin and dest_belfast):
        return "Enterprise"
    
    # DART routes (all within Dublin coastal area)
    dart_stations = [
        'MALAHIDE', 'PORTMARNOCK', 'CLONGRIFFIN', 'HOWTH', 'SUTTON', 'LAYTOWN',
        'BALBRIGGAN', 'SKERRIES', 'MOUNT MERRION', 'BAYSIDE', 'KILLESTER', 'HARMONSTOWN', 
        'RAHENY', 'KILBARRACK','CLONTARF', 'CONNOLLY', 'TARA STREET', 'PEARSE', 'GRAND CANAL',
        'LANSDOWNE', 'SANDYMOUNT', 'SYDNEY PARADE', 'BOOTERSTOWN',
        'BLACKROCK', 'SEAPOINT', 'SALTHILL', 'DUN LAOGHAIRE', 'SANDYCOVE',
        'GLENAGEARY', 'DALKEY', 'KILLINEY', 'SHANKILL', 'BRAY', 'GREYSTONES', 'DROGHEDA'
    ]
    
    origin_is_dart = any(station in origin_str for station in dart_stations)
    dest_is_dart = any(station in dest_str for station in dart_stations)
    
    if origin_is_dart and dest_is_dart:
        return "DART"
    
    # Major intercity routes (not Enterprise)
    major_cities = ['CORK', 'GALWAY', 'LIMERICK', 'WATERFORD', 'SLIGO', 'TRALEE']
    dublin_terminals = ['CONNOLLY', 'HEUSTON']
    
    origin_major = any(city in origin_str for city in major_cities)
    dest_major = any(city in dest_str for city in major_cities)
    origin_dublin_terminal = any(term in origin_str for term in dublin_terminals)
    dest_dublin_terminal = any(term in dest_str for term in dublin_terminals)
    
    if (origin_major and dest_dublin_terminal) or (origin_dublin_terminal and dest_major):
        return "Intercity"
    
    # Dublin commuter (not DART)
    if origin_dublin_terminal or dest_dublin_terminal:
        return "Commuter"
    
    return "Regional"


# Train type from public message
def train_type_from_message(public_message):
    """
    Extract hints from public message
    """
    if pd.isna(public_message):
        return "Unknown"
    
    message = str(public_message).upper()
    
    # Look for service type mentions
    if 'DART' in message:
        return "DART"
    if 'ENTERPRISE' in message:
        return "Enterprise"
    if 'INTERCITY' in message:
        return "Intercity"
    
    return "Unknown"


# Add train types to DataFrame
def add_train_types(df):
    """
    Add train types to any DataFrame with train data
    """
    if df.empty:
        return df
    
    updated_df = df.copy()
    
    # Method 1: From train code 
    if 'TrainCode' in df.columns:
        updated_df['train_type_code'] = df['TrainCode'].apply(train_type_from_code)
    
    # Method 2: From route 
    if 'TrainOrigin' in df.columns and 'TrainDestination' in df.columns:
        updated_df['route_type'] = df.apply(
            lambda row: train_type_from_route(row['TrainOrigin'], row['TrainDestination']), axis=1
        )
    
    # Method 3: From public message
    if 'PublicMessage' in df.columns:
        updated_df['message_type'] = df['PublicMessage'].apply(train_type_from_message)
    
    # Using the route type as primary
    if 'route_type' in updated_df.columns:
        updated_df['train_type'] = updated_df['route_type']
        
        # Only use code-based if route gives Unknown
        mask = updated_df['train_type'] == 'Unknown'
        if 'train_type_code' in updated_df.columns:
            updated_df.loc[mask, 'train_type'] = updated_df.loc[mask, 'train_type_code']
    else:
        updated_df['train_type'] = updated_df.get('train_type_code', 'Unknown')
    


    # Clean up E_Code_Unknown (these should be resolved by route)
    mask = updated_df['train_type'] == 'E_Code_Unknown'
    updated_df.loc[mask, 'train_type'] = 'Unknown'
    
    # Override with message type if still Unknown
    if 'message_type' in updated_df.columns:
        mask = updated_df['train_type'] == 'Unknown'
        updated_df.loc[mask, 'train_type'] = updated_df.loc[mask, 'message_type']
    
    return updated_df

# Summary of train types
def get_train_type_summary(df):
    """
    Get a summary of train types in the data
    """
    if 'train_type' in df.columns:
        type_counts = df['train_type'].value_counts()
        print("Train Type Distribution:")
        print(type_counts)
        return type_counts
    else:
        print("No train types found")
        return None



