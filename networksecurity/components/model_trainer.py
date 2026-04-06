import os
import sys
import numpy as np

from sklearn.linear_model import LogisticRegression

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from networksecurity.utils.main_utils.utils import save_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


class ModelTrainer:
    def __init__(self,
                 model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):

        try:
            self.config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logger.info("Starting Model Training")

            # =========================
            # LOAD DATA
            # =========================
            train_arr = np.load(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = np.load(self.data_transformation_artifact.transformed_test_file_path)

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            # =========================
            # MODEL TRAIN
            # =========================
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)

            # =========================
            # PREDICT
            # =========================
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # =========================
            # METRICS (🔥 NEW)
            # =========================
            train_metric = get_classification_score(y_train, y_train_pred)
            test_metric = get_classification_score(y_test, y_test_pred)

            logger.info(f"Train Metric: {train_metric}")
            logger.info(f"Test Metric: {test_metric}")

            # =========================
            # LOAD PREPROCESSOR
            # =========================
            import pickle
            with open(self.data_transformation_artifact.preprocessor_object_file_path, "rb") as f:
                preprocessor = pickle.load(f)

            # =========================
            # WRAP MODEL (🔥 NEW)
            # =========================
            network_model = NetworkModel(preprocessor=preprocessor, model=model)

            # =========================
            # SAVE MODEL
            # =========================
            save_object(self.config.trained_model_file_path, network_model)

            logger.info("Model saved successfully")

            return ModelTrainerArtifact(
                trained_model_file_path=self.config.trained_model_file_path,
                train_metric=train_metric.f1_score,
                test_metric=test_metric.f1_score
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)