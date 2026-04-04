# This module is responsible for validating the data schema of the ingested data.
# It reads the training and testing data files, checks if they conform to the expected schema defined in a YAML file,
# and saves the valid data files to a specified directory. It also returns an artifact containing the validation status and file paths.
# The validation process ensures that the data used for training and testing the model is consistent and meets the required format before proceeding to the next steps in the pipeline.

#location 
# networksecurity/components/data_validation.py

import os
import sys
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig):
        try:
            self.config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = len(self._schema_config["columns"])
            actual_columns = len(dataframe.columns)

            logger.info(f"Expected columns: {expected_columns}")
            logger.info(f"Actual columns: {actual_columns}")

            return expected_columns == actual_columns

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                test = ks_2samp(d1, d2)

                if test.pvalue < threshold:
                    drift = True
                    status = False
                else:
                    drift = False

                report[column] = {
                    "p_value": float(test.pvalue),
                    "drift_status": drift
                }

            drift_path = self.config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_path), exist_ok=True)

            write_yaml_file(drift_path, report)

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_df = self.read_data(self.config.train_file_path)
            test_df = self.read_data(self.config.test_file_path)

            if not self.validate_number_of_columns(train_df):
                raise Exception("Train columns mismatch")

            if not self.validate_number_of_columns(test_df):
                raise Exception("Test columns mismatch")

            drift_status = self.detect_dataset_drift(train_df, test_df)

            os.makedirs(os.path.dirname(self.config.valid_train_file_path), exist_ok=True)

            train_df.to_csv(self.config.valid_train_file_path, index=False)
            test_df.to_csv(self.config.valid_test_file_path, index=False)

            logger.info("Data Validation Completed")

            return DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.config.valid_train_file_path,
                valid_test_file_path=self.config.valid_test_file_path,
                invalid_train_file_path=self.config.invalid_train_file_path,
                invalid_test_file_path=self.config.invalid_test_file_path,
                drift_report_file_path=self.config.drift_report_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)