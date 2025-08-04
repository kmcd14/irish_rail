import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")

try:
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Connected. Current Time:", result)
    cursor.close()
    conn.close()
except Exception as e:
    print("Error connecting to the database:", e)