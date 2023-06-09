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
    target_encoder_path:str

@dataclass
class ModelTrainerArtifact:
    model_file_path:str
    r2_score_train:float
    r2_score_test:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str
    saved_model_dir:str
