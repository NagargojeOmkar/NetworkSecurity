from dataclasses import dataclass


# =========================
# DATA INGESTION ARTIFACT
# =========================

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str