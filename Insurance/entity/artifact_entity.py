import os
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_filepath:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transform_train_path:str
    transform_test_path:str