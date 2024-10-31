import sqlite3
import pandas as pd
from google.cloud import storage
import os

# Set up your Google Cloud Storage bucket and credentials
BUCKET_NAME = 'nhc-csv'
PROJECT_ID = 'cse-6242-fa24-lz'

# Initialize the GCS client
client = storage.Client(project=PROJECT_ID)
bucket = client.get_bucket(BUCKET_NAME)

# Connect to SQLite database and enable Spatialite extension
conn = sqlite3.connect("nhc.sqlite")
conn.enable_load_extension(True)

try:
    conn.execute("SELECT load_extension('mod_spatialite')")
    print("Spatialite extension loaded successfully.")
except sqlite3.OperationalError as e:
    print(f"Error loading Spatialite extension: {e}")
    conn.close()
    raise

cursor = conn.cursor()

# Fetch all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Export each table to a separate CSV file and upload to GCS
for table_name in tables:
    table_name = table_name[0]
    try:
        # Export table to CSV
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        csv_file_path = f"{table_name}.csv"
        df.to_csv(csv_file_path, index=False)
        print(f"Exported {table_name} to {csv_file_path}")

        # Upload CSV to GCS
        blob = bucket.blob(f"{table_name}.csv")
        blob.upload_from_filename(csv_file_path)
        print(f"Uploaded {table_name}.csv to GCS bucket {BUCKET_NAME}")

        # Optionally, delete the local CSV file after upload
        os.remove(csv_file_path)

    except Exception as e:
        print(f"Error exporting or uploading table {table_name}: {e}")

conn.close()
