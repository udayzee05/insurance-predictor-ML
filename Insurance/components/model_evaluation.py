import sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity import config_entity,artifact_entity
from Insurance.predictor import ModelResolver



class ModelEvaluation:
    def __init__(self,model_evaluation_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact

            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            logging.info(f"{'>>'*5} Model Evaluation {'<<'*5}")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact

        except Exception as e:
            raise InsuranceException(e, sys)
        
