from dataclasses import dataclass


# =========================
# DATA INGESTION ARTIFACT
# =========================

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str


# =========================
# DATA VALIDATION ARTIFACT
# =========================

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


# =========================
# DATA TRANSFORMATION ARTIFACT
# =========================

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessor_object_file_path: str

# =========================
# MODEL TRAINER ARTIFACT
# =========================

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric: ClassificationMetricArtifact
    test_metric: ClassificationMetricArtifact

    


