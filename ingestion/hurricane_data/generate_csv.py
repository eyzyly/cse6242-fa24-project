import sqlite3
import pandas as pd
from google.cloud import storage, bigquery
import os
from shapely import wkb

# Set up your Google Cloud Storage bucket and credentials
BUCKET_NAME = 'nhc-csv-test'
FOLDER_NAME = 'test'
PROJECT_ID = 'cse-6242-fa24-lz'
DATASET_NAME = 'hurricane_data'  # Change this to your desired dataset name

# Initialize the GCS client
storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.get_bucket(BUCKET_NAME)

# Initialize the BigQuery client
bigquery_client = bigquery.Client(project=PROJECT_ID)

# Create dataset in us-east1 region
def create_dataset():
    dataset_ref = bigquery_client.dataset(DATASET_NAME)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "us-east1"
    try:
        bigquery_client.create_dataset(dataset)
        print(f"Dataset {DATASET_NAME} created in {dataset.location} region.")
    except Exception as e:
        print(f"Error creating dataset: {e}")

create_dataset()

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
        # Fetch the column names to check for geometry
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        geometry_columns = [col[1] for col in columns if col[2] == 'GEOMETRY']
        
        # Prepare the SQL query to select geometry columns as WKT
        if geometry_columns:
            select_clause = ", ".join([f"ASText({col}) AS {col}" for col in geometry_columns])
            sql_query = f"SELECT *, {select_clause} FROM {table_name}"
        else:
            sql_query = f"SELECT * FROM {table_name}"

        # Export table to DataFrame
        df = pd.read_sql_query(sql_query, conn)

        # Convert geometry byte strings to Shapely geometries and then to WKT
        for col in geometry_columns:
            df[col] = df[col].apply(lambda geom: wkb.loads(geom, hex=True).wkt if isinstance(geom, bytes) else geom)

        print(df.head())
        csv_file_path = f"{table_name}.csv"
        df.to_csv(csv_file_path, index=False)
        print(f"Exported {table_name} to {csv_file_path}")

        # Upload CSV to GCS in the specified folder
        blob = bucket.blob(f"{FOLDER_NAME}/{table_name}.csv")  # Updated path to include folder
        blob.upload_from_filename(csv_file_path)
        print(f"Uploaded {table_name}.csv to GCS bucket {BUCKET_NAME}/{FOLDER_NAME}")

        # Optionally, delete the local CSV file after upload
        os.remove(csv_file_path)

    except Exception as e:
        print(f"Error exporting or uploading table {table_name}: {e}")

conn.close()
