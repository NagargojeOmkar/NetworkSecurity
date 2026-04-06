import sys

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException

# Components
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig

# Configs
from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataValidationConfig
)


def start_pipeline():
    try:
        logger.info("=== Training Pipeline Started ===")

        # =========================
        # STEP 1: DATA INGESTION
        # =========================
        logger.info("Step 1: Data Ingestion Started")

        data_ingestion = DataIngestion()
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logger.info(f"Data Ingestion Completed: {data_ingestion_artifact}")

        # =========================
        # STEP 2: CONFIGURATION
        # =========================
        training_pipeline_config = TrainingPipelineConfig()

        # =========================
        # STEP 3: DATA VALIDATION
        # =========================
        logger.info("Step 2: Data Validation Started")

        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config,
            data_ingestion_artifact=data_ingestion_artifact
        )

        data_validation = DataValidation(data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()

        logger.info(f"Data Validation Completed: {data_validation_artifact}")

        # =========================
        # STEP 4: DATA TRANSFORMATION
        # =========================
        logger.info("Step 3: Data Transformation Started")

        data_transformation = DataTransformation(
            training_pipeline_config=training_pipeline_config,
            data_validation_artifact=data_validation_artifact
        )

        data_transformation_artifact = data_transformation.initiate_data_transformation()

        logger.info(f"Data Transformation Completed: {data_transformation_artifact}")

        logger.info("=== Training Pipeline Completed Successfully ===")

        # =========================
        # STEP 5: MODEL TRAINING
        # =========================

        logger.info("Step 4: Model Training Started")

        model_trainer_config = ModelTrainerConfig(training_pipeline_config)

        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact
        )

        model_trainer_artifact = model_trainer.initiate_model_trainer()

        logger.info(f"Model Training Completed: {model_trainer_artifact}")
        
        

    except Exception as e:
        logger.error("Pipeline Failed")
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    start_pipeline()