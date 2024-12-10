import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create a database connection pool
def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection