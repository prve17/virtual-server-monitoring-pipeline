import os
import logging
import hashlib
import pandas as pd
from sqlalchemy import create_engine
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import urllib

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Environment variables
BLOB_CONNECTION = os.getenv("AZURE_BLOB_CONNECTION_STRING")
SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")
CONTAINER = os.getenv("BLOB_CONTAINER")
BLOB_FILE = os.getenv("BLOB_FILE")


def download_blob():
    try:
        logging.info("Connecting to Azure Blob Storage...")

        blob_service_client = BlobServiceClient.from_connection_string(
            BLOB_CONNECTION
        )

        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER,
            blob=BLOB_FILE
        )

        with open("server_logs.csv", "wb") as file:
            data = blob_client.download_blob()
            file.write(data.readall())

        logging.info("File downloaded successfully")

    except Exception as e:
        logging.error("Blob download failed: %s", e)
        raise


def transform_data():
    try:
        logging.info("Loading dataset")

        df = pd.read_csv("server_logs.csv")

        df.columns = [
            "server_id",
            "hostname",
            "ip_address",
            "os_type",
            "server_location",
            "cpu_utilization",
            "memory_usage",
            "disk_io",
            "network_traffic_in",
            "network_traffic_out",
            "uptime_hours",
            "downtime_hours",
            "admin_name",
            "admin_email",
            "admin_phone",
            "log_timestamp"
        ]

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove missing server IDs
        df = df.dropna(subset=["server_id"])

        df["admin_email"] = df["admin_email"].str.replace(r'.+@', '***@', regex=True)

        # Convert timestamp
        df["log_timestamp"] = pd.to_datetime(
            df["log_timestamp"],
            dayfirst=True
        )

        # CPU status
        def cpu_status(x):
            if x > 85:
                return "High"
            elif x > 60:
                return "Medium"
            return "Normal"

        df["cpu_status"] = df["cpu_utilization"].apply(cpu_status)

        # Memory status
        def memory_status(x):
            if x > 80:
                return "High"
            elif x > 60:
                return "Medium"
            return "Normal"

        df["memory_status"] = df["memory_usage"].apply(memory_status)

        # Resource utilization score
        df["resource_utilization_score"] = (
            df["cpu_utilization"] +
            df["memory_usage"]
        ) / 2

        # PII masking example (hash IP)
        df["ip_address"] = df["ip_address"].apply(
            lambda x: hashlib.sha256(x.encode()).hexdigest()
        )

        logging.info("Data transformation completed")

        return df

    except Exception as e:
        logging.error("Transformation failed: %s", e)
        raise


def load_to_sql(df):
    try:
        logging.info("Connecting to Azure SQL Database")

        params = urllib.parse.quote_plus(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USERNAME};"
            f"PWD={SQL_PASSWORD};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )

        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}"
        )

        df.to_sql(
            "server_metrics",
            con=engine,
            if_exists="append",
            index=False
        )

        logging.info("Data loaded successfully into Azure SQL")

    except Exception as e:
        logging.error("Database load failed: %s", e)
        raise


def main():

    logging.info("Starting Server Monitoring Pipeline")

    download_blob()

    df = transform_data()

    load_to_sql(df)

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
