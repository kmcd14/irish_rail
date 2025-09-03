# Insert data into the database
#from sqlalchemy import create_engine
#from scripts.conn import DB_CONFIG
#
#engine = create_engine(f"postgresql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['DBNAME']}")
#
#def insert_data(df, table_name):
#    """
#    Insert data into the specified table in the database.
#    """
#    try:
#       df.to_sql(table_name, con=engine, index=False, if_exists='append')
#       print(f"Data inserted into {table_name} successfully.")
#
#    except Exception as e:
#        print(f"Error inserting data into {table_name}: {e}")

# Insert data into the database
from sqlalchemy import create_engine, text
from datetime import datetime
from scripts.conn import DB_CONFIG
import pandas as pd

engine = create_engine(f"postgresql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['DBNAME']}")

def insert_data(df, table_name):
    """
    Insert data into the specified table in the database with duplicate handling
    that preserves historical data.
    """
    try:
        if table_name == 'stations':
            # For stations, replace all data since it changes rarely
            df.to_sql(table_name, con=engine, index=False, if_exists='replace')
            print(f"Replaced {len(df)} records in {table_name} successfully.")
            
        elif table_name == 'current_trains':
            # For current trains, we want the latest snapshot, so replace today's data
            today = datetime.now().date()
            
            with engine.connect() as conn:
                delete_query = text('DELETE FROM current_trains WHERE "TrainDate" = :today')
                result = conn.execute(delete_query, {"today": today})
                deleted_count = result.rowcount
                
                if deleted_count > 0:
                    print(f"Deleted {deleted_count} existing current train records for {today}")
                
                df.to_sql(table_name, con=conn, index=False, if_exists='append', method='multi')
                conn.commit()
                
            print(f"Successfully loaded {len(df)} current train records")
            
        elif table_name == 'train_movements':
            # For train movements, use UPSERT to preserve historical data
            # but update records if they already exist
            _upsert_train_movements(df)
            
        else:
            # For other tables append
            df.to_sql(table_name, con=engine, index=False, if_exists='append')
            print(f"Data inserted into {table_name} successfully.")

    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        raise

def _upsert_train_movements(df):
    """
    Alternative UPSERT using individual record processing.
    Slower but more reliable for data type issues.
    """
    if df.empty:
        return
        
    try:
        with engine.connect() as conn:
            upserted_count = 0
            
            for _, row in df.iterrows():
                # Convert row to dict and handle data types
                record = row.to_dict()
                
                # Ensure proper types
                if 'LocationOrder' in record:
                    record['LocationOrder'] = int(float(record['LocationOrder'])) if pd.notna(record['LocationOrder']) else 1
                if 'delay_minutes' in record:
                    record['delay_minutes'] = int(float(record['delay_minutes'])) if pd.notna(record['delay_minutes']) else None
                
                # Build column lists
                columns = list(record.keys())
                placeholders = [f':{col}' for col in columns]
                
                primary_key_cols = ['TrainCode', 'TrainDate', 'LocationOrder']
                update_cols = [col for col in columns if col not in primary_key_cols]
                set_clause = ', '.join([f'"{col}" = EXCLUDED."{col}"' for col in update_cols])
                
                # Individual UPSERT query
                query = text(f'''
                    INSERT INTO train_movements ({', '.join([f'"{col}"' for col in columns])})
                    VALUES ({', '.join(placeholders)})
                    ON CONFLICT ("TrainCode", "TrainDate", "LocationOrder")
                    DO UPDATE SET {set_clause}
                ''')
                
                conn.execute(query, record)
                upserted_count += 1
            
            conn.commit()
            print(f"Successfully upserted {upserted_count} train movement records")
            
    except Exception as e:
        print(f"Failed to upsert train movements: {e}")
        raise


# Only insert truly new records
#def _insert_only_new_movements(df):
#    """
#    Insert only records that don't already exist in the database.
#    This preserves all historical data without updates.
#    """
#    if df.empty:
#        return
#        
#    try:
#        with engine.connect() as conn:
#            # Create temporary table
#            temp_table = f"temp_new_movements_{int(datetime.now().timestamp())}"
#            df.to_sql(temp_table, con=conn, index=False, if_exists='replace', method='multi')
#            
#            # Insert only records that don't exist
#            insert_query = text(f'''
#                INSERT INTO train_movements 
#                SELECT t.* FROM {temp_table} t
#                WHERE NOT EXISTS (
#                    SELECT 1 FROM train_movements tm 
#                    WHERE tm."TrainCode" = t."TrainCode" 
#                    AND tm."TrainDate" = t."TrainDate" 
#                    AND tm."LocationOrder" = t."LocationOrder"
#                )
#            ''')
#            
#            result = conn.execute(insert_query)
#            inserted_count = result.rowcount
#            
#            # Clean up
#            conn.execute(text(f'DROP TABLE {temp_table}'))
#            conn.commit()
#            
#            print(f"Inserted {inserted_count} new train movement records (skipped duplicates)")
#            
#    except Exception as e:
#        print(f"Failed to insert new movements: {e}")
#        raise