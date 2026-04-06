import os
from datetime import datetime
from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.testing_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self,
                 training_pipeline_config: TrainingPipelineConfig,
                 data_ingestion_artifact):

        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        # VALID DATA
        self.valid_data_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        self.valid_train_file_path = os.path.join(
            self.valid_data_dir,
            "train.csv"
        )

        self.valid_test_file_path = os.path.join(
            self.valid_data_dir,
            "test.csv"
        )

        # INVALID DATA
        self.invalid_data_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        self.invalid_train_file_path = os.path.join(
            self.invalid_data_dir,
            "train.csv"
        )

        self.invalid_test_file_path = os.path.join(
            self.invalid_data_dir,
            "test.csv"
        )

        # DRIFT REPORT
        self.drift_report_file_path = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

        # INPUT FROM INGESTION
        self.train_file_path = data_ingestion_artifact.trained_file_path
        self.test_file_path = data_ingestion_artifact.test_file_path



class dataTransformationConfig:
    def __init__(self,
                 training_pipeline_config: TrainingPipelineConfig,
                 data_validation_artifact):

        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )

        self.transformed_train_file_path = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy")
        )
        self.transformed_test_file_path = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy")
        )
        self.transformed_object_file_path = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.DATA_TRANSFORMATION_OBJECT_FILE_NAME
        )
        self.valid_train_file_path = data_validation_artifact.valid_train_file_path
        self.valid_test_file_path = data_validation_artifact.valid_test_file_path
        self.valid_transformed_file_path = data_validation_artifact.valid_transformed_file_path
        
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config):

        self.model_trainer_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_DIR_NAME
        )

        self.trained_model_file_path = os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_FILE_NAME
        )

        self.expected_accuracy = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = (
            training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
        )   

