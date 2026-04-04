# networksecurity/pipeline/data_ingestion.py

import os
import sys
import pandas as pd
import numpy as np
import pymongo

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    TrainingPipelineConfig
)

from networksecurity.entity.artifact_entity import DataIngestionArtifact


MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # FIXED


class DataIngestion:
    def __init__(self):
        try:
            training_pipeline_config = TrainingPipelineConfig()
            self.config = DataIngestionConfig(training_pipeline_config)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        try:
            client = pymongo.MongoClient(MONGO_DB_URL)

            db = client[self.config.database_name]
            collection = db[self.config.collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            logger.info(f"Data fetched from MongoDB | shape: {df.shape}")

            if df.shape[0] == 0:
                raise Exception("No data found in MongoDB")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            path = self.config.feature_store_file_path
            os.makedirs(os.path.dirname(path), exist_ok=True)

            dataframe.to_csv(path, index=False)
            logger.info("Data saved to feature store")

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.config.train_test_split_ratio,
                random_state=42
            )

            dir_path = os.path.dirname(self.config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(self.config.training_file_path, index=False)
            test_set.to_csv(self.config.testing_file_path, index=False)

            logger.info("Train-test split done")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)

            logger.info("Data ingestion completed")

            return DataIngestionArtifact(
                trained_file_path=self.config.training_file_path,
                test_file_path=self.config.testing_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)