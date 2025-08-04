# Insert data into the database
from sqlalchemy import create_engine
from conn import DB_CONFIG

engine = create_engine(f"postgresql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['DBNAME']}")

def insert_data(df, table_name):
    """
    Insert data into the specified table in the database.
    """
    try:
       df.to_sql(table_name, con=engine, index=False, if_exists='append')
       print(f"Data inserted into {table_name} successfully.")

    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")