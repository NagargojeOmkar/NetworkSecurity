import sys

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.data_ingestion import DataIngestion


def start_pipeline():
    try:
        logger.info("Training pipeline started")

        # Step 1: Data Ingestion
        data_ingestion = DataIngestion()
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

        logger.info("Training pipeline completed successfully")

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    start_pipeline()