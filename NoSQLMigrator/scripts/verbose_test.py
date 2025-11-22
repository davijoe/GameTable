import sys
import os
import mysql.connector
from pymongo import MongoClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("STARTING VERBOSE CONNECTION TEST")
print("=" * 50)

from dotenv import load_dotenv
load_dotenv()

print("Environment variables:")
print(f"  MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"  MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE')}")
print(f"  MONGODB_HOST: {os.getenv('MONGODB_HOST')}")
print()

print("1. Testing MySQL Connection...")
try:
    mysql_conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        database=os.getenv('MYSQL_DATABASE', 'gametable'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        connection_timeout=5
    )
    
    cursor = mysql_conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"   SUCCESS: Connected to MySQL")
    print(f"   Found {len(tables)} tables")
    for table in tables[:5]: 
        print(f"      - {table[0]}")
    if len(tables) > 5:
        print(f"      ... and {len(tables) - 5} more")
    
    cursor.close()
    mysql_conn.close()
    
except Exception as e:
    print(f"   FAILED: MySQL connection error: {e}")

print()

print("2. Testing MongoDB Connection...")
try:
    mongo_conn_str = f"mongodb://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGODB_HOST')}:{os.getenv('MONGODB_PORT')}/"
    mongo_client = MongoClient(mongo_conn_str, serverSelectionTimeoutMS=5000)
    
    mongo_client.admin.command('ping')
    print(f"   SUCCESS: Connected to MongoDB")
    
    dbs = mongo_client.list_database_names()
    print(f"   Found {len(dbs)} databases")
    for db in dbs[:5]:
        print(f"      - {db}")
    
    mongo_client.close()
    
except Exception as e:
    print(f"   FAILED: MongoDB connection error: {e}")

print("=" * 50)
print("TEST COMPLETED")