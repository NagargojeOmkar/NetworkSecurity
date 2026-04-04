# push_data.py

import os
import sys
import pandas as pd
import pymongo
import certifi

from dotenv import load_dotenv
load_dotenv()

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException


class DataPush:
    def __init__(self, file_path: str, database: str, collection: str):
        self.file_path = file_path
        self.database = database
        self.collection = collection

        # MongoDB connection
        self.mongo_uri = os.getenv("MONGO_DB_URL")
        self.ca = certifi.where()

        if not self.mongo_uri:
            raise Exception("❌ MONGO_DB_URL not found in .env file")

    def load_data(self) -> pd.DataFrame:
        """Load CSV data"""
        try:
            logger.info("Loading data from CSV...")

            if not os.path.exists(self.file_path):
                raise Exception(f"File not found: {self.file_path}")

            df = pd.read_csv(self.file_path)

            logger.info(f"Data loaded | shape: {df.shape}")
            print(f"Loaded data: {df.shape} ✅")

            if df.shape[0] == 0:
                raise Exception("CSV file is empty ❌")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def connect_mongodb(self):
        """Create MongoDB connection"""
        try:
            logger.info("Connecting to MongoDB...")

            client = pymongo.MongoClient(self.mongo_uri, tlsCAFile=self.ca)

            # Test connection
            client.admin.command('ping')

            logger.info("MongoDB connection successful")
            print("MongoDB connected ✅")

            return client

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def push_to_mongodb(self, df: pd.DataFrame):
        """Push data to MongoDB"""
        try:
            client = self.connect_mongodb()

            db = client[self.database]
            collection = db[self.collection]

            # 🔥 Check collections
            print("Available collections:", db.list_collection_names())

            # 🔥 Clear old data
            collection.delete_many({})
            logger.info("Old data cleared from collection")
            print("Old data cleared ✅")

            # Convert DataFrame → dict
            data = df.to_dict(orient="records")

            if len(data) == 0:
                raise Exception("No data to insert ❌")

            # Insert data
            result = collection.insert_many(data)

            inserted_count = len(result.inserted_ids)

            logger.info(f"Inserted {inserted_count} records into MongoDB")
            print(f"Inserted {inserted_count} records into MongoDB")

            # 🔥 Verify insertion
            count = collection.count_documents({})
            print(f"Total documents in DB: {count}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        FILE_PATH = "Network_data/phisingData.csv"
        DATABASE = "networksecurity"
        COLLECTION = "data"

        print("🚀 Starting Data Push Pipeline...\n")

        data_push = DataPush(FILE_PATH, DATABASE, COLLECTION)

        df = data_push.load_data()

        data_push.push_to_mongodb(df)

        print("\n🎯 Data push completed successfully!")
        logger.info("Data push pipeline completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)