import sys

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation

from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig


def start_pipeline():
    try:
        logger.info("Training pipeline started")

        # 🔥 STEP 1: Data Ingestion
        data_ingestion = DataIngestion()
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

        # 🔥 STEP 2: Create Training Config
        training_pipeline_config = TrainingPipelineConfig()

        # 🔥 STEP 3: Create Validation Config
        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config,
            data_ingestion_artifact=data_ingestion_artifact
        )

        # 🔥 STEP 4: Data Validation
        logger.info("Data Validation started")

        data_validation = DataValidation(data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()

        logger.info(f"Data Validation Artifact: {data_validation_artifact}")

        logger.info("Training pipeline completed successfully")

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    start_pipeline()