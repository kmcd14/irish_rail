# Clean data from the Irish Rail API
from datetime import datetime
import pandas as pd


### Convert data types ###


# convert object type date columns to datetime
def object_to_date(df, columns):
    """
    Convert object type date columns to datetime.
    """
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


# convert object type to time
def object_to_time(df, columns):
    """
    Convert object columns to Python time objects.
    """
    for col in columns:
        df[col] = pd.to_datetime(df[col], format='%H:%M:%S', errors='coerce').dt.time
    return df



# convert object type columns to string
def object_tostring(df, columns):
    """
    Convert object type columns to string.
    """
    for col in columns:
        df[col] = df[col].astype('string')
    return df


# convert object type columns to float
def object_to_float(df, columns):
    """
    Convert object type columns to float.
    """
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
    

# timestamp of fetch
def fetch_timestamp():
    """
    Get the current timestamp and insert it into the DataFrame.
    This function returns the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



##############################################


### Cleaning functions ###

# remove whitespace from string columns
def remove_whitespace(df, columns):
    """
    Remove leading and trailing whitespace from string columns.
    """
    for col in columns:
        df[col] = df[col].str.strip()
    return df


# remove rows with Null values in specified columns
def remove_nulls(df, columns):
    """
    Remove rows with Null values in specified columns.
    """
    for col in columns:
        df = df[df[col].notnull()]
    return df

# remove line breaks 
def remove_linebreaks(df, columns):
    """
    Remove line breaks from string columns.
    """
    for col in columns:
         df[col] = df[col].str.replace(r'(\\n|\n)', ' ', regex=True).str.strip()
    return df

# cleaning.py (or ncleaning.py)

def remove_duplicates(df, subset_columns):
    """
    Remove duplicate rows from the DataFrame based on the subset of columns.
        
    """
    return df.drop_duplicates(subset=subset_columns)
