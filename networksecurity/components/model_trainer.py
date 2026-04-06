import sys
import numpy as np
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)
from sklearn.model_selection import GridSearchCV

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact

from networksecurity.utils.main_utils.utils import save_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


class ModelTrainer:
    def __init__(self, model_trainer_config, data_transformation_artifact):
        try:
            self.config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logger.info("Starting Multi-Model Training")

            # =========================
            # LOAD DATA
            # =========================
            train_arr = np.load(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = np.load(self.data_transformation_artifact.transformed_test_file_path)

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            # =========================
            # MODELS
            # =========================
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "AdaBoost": AdaBoostClassifier()
            }

            # =========================
            # PARAM GRIDS
            # =========================
            param_grids = {
                "Logistic Regression": {
                    "C": [0.01, 0.1, 1, 10],
                    "solver": ["liblinear", "lbfgs"]
                },
                "Decision Tree": {
                    "criterion": ["gini", "entropy", "log_loss"]
                },
                "Random Forest": {
                    "n_estimators": [16, 32, 64, 128]
                },
                "Gradient Boosting": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.05, 0.1]
                },
                "AdaBoost": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.5, 1.0]
                }
            }

            best_model = None
            best_score = -1
            best_model_name = None

            # =========================
            # TRAIN ALL MODELS
            # =========================
            for model_name, model in models.items():
                logger.info(f"Training {model_name}")

                param_grid = param_grids[model_name]

                grid = GridSearchCV(
                    estimator=model,
                    param_grid=param_grid,
                    cv=5,
                    scoring="f1",
                    n_jobs=-1
                )

                grid.fit(X_train, y_train)

                trained_model = grid.best_estimator_

                y_test_pred = trained_model.predict(X_test)
                metric = get_classification_score(y_test, y_test_pred)

                logger.info(f"{model_name} F1 Score: {metric.f1_score}")

                # BEST MODEL SELECT
                if metric.f1_score > best_score:
                    best_score = metric.f1_score
                    best_model = trained_model
                    best_model_name = model_name

            logger.info(f"Best Model: {best_model_name} with F1 Score: {best_score}")

            # =========================
            # FINAL METRICS
            # =========================
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            train_metric = get_classification_score(y_train, y_train_pred)
            test_metric = get_classification_score(y_test, y_test_pred)

            # =========================
            # LOAD PREPROCESSOR
            # =========================
            with open(self.data_transformation_artifact.preprocessor_object_file_path, "rb") as f:
                preprocessor = pickle.load(f)

            # =========================
            # WRAP MODEL
            # =========================
            final_model = NetworkModel(preprocessor, best_model)

            # =========================
            # SAVE MODEL
            # =========================
            save_object(self.config.trained_model_file_path, final_model)

            logger.info("Best model saved successfully")

            return ModelTrainerArtifact(
                trained_model_file_path=self.config.trained_model_file_path,
                train_metric=train_metric,
                test_metric=test_metric
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)