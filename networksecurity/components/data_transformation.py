import os
import sys
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from networksecurity.constant import training_pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self,
                 training_pipeline_config: TrainingPipelineConfig,
                 data_validation_artifact: DataValidationArtifact):

        try:
            self.training_pipeline_config = training_pipeline_config
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        try:
            logger.info("Creating preprocessing pipeline")

            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            scaler = StandardScaler()

            pipeline = Pipeline(steps=[
                ("imputer", imputer),
                ("scaler", scaler)
            ])

            return pipeline

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info("Starting Data Transformation")

            # =========================
            # READ VALIDATED DATA
            # =========================
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            logger.info(f"Train shape: {train_df.shape}")
            logger.info(f"Test shape: {test_df.shape}")

            # =========================
            # SPLIT FEATURES & TARGET
            # =========================
            X_train = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_train = train_df[TARGET_COLUMN]

            X_test = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_test = test_df[TARGET_COLUMN]

            # =========================
            # CREATE PIPELINE
            # =========================
            transformer = self.get_data_transformer_object()

            # =========================
            # FIT & TRANSFORM
            # =========================
            X_train_transformed = transformer.fit_transform(X_train)
            X_test_transformed = transformer.transform(X_test)

            logger.info("Data transformed successfully")

            # =========================
            # COMBINE X + y
            # =========================
            train_array = np.c_[X_train_transformed, y_train.to_numpy()]
            test_array = np.c_[X_test_transformed, y_test.to_numpy()]

            # =========================
            # FILE PATHS (CORRECT WAY)
            # =========================
            transformed_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                training_pipeline.DATA_TRANSFORMATION_DIR_NAME,
                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR
            )

            object_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                training_pipeline.DATA_TRANSFORMATION_DIR_NAME,
                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR
            )

            train_file_path = os.path.join(transformed_dir, "train.npy")
            test_file_path = os.path.join(transformed_dir, "test.npy")

            preprocessor_path = os.path.join(
                object_dir,
                training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
            )

            # =========================
            # SAVE FILES
            # =========================
            save_numpy_array_data(train_file_path, train_array)
            save_numpy_array_data(test_file_path, test_array)

            save_object(preprocessor_path, transformer)

            logger.info("Saved transformed data and preprocessing object")

            # =========================
            # RETURN ARTIFACT
            # =========================
            return DataTransformationArtifact(
                transformed_train_file_path=train_file_path,
                transformed_test_file_path=test_file_path,
                preprocessor_object_file_path=preprocessor_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)