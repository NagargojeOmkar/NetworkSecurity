import os
import sys
import pandas as pd
import pymongo
import certifi

from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env file

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import CustomException


class DataPush:
    def __init__(self, file_path: str, database: str, collection: str):
        self.file_path = file_path
        self.database = database
        self.collection = collection

        # MongoDB connection
        self.mongo_uri = os.getenv("MONGO_URI")
        self.ca = certifi.where()

    def load_data(self) -> pd.DataFrame:
        """Load CSV data into DataFrame"""
        try:
            df = pd.read_csv(self.file_path)
            logger.info("Data loaded successfully from CSV")
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def push_to_mongodb(self, df: pd.DataFrame):
        """Push DataFrame to MongoDB"""
        try:
            client = pymongo.MongoClient(self.mongo_uri, tlsCAFile=self.ca)
            db = client[self.database]
            collection = db[self.collection]

            # Convert DataFrame to dict
            data = df.to_dict(orient="records")

            # Insert data
            collection.insert_many(data)
            logger.info("Data successfully pushed to MongoDB")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        # Example usage
        FILE_PATH = "Network_data/phisingData.csv"   # update path if needed
        DATABASE = "networksecurity"
        COLLECTION = "data"

        data_push = DataPush(FILE_PATH, DATABASE, COLLECTION)

        df = data_push.load_data()
        data_push.push_to_mongodb(df)

        logger.info("Data push pipeline completed")

    except Exception as e:
        raise CustomException(e, sys)