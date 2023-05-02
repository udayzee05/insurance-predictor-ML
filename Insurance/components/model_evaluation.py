import sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity import config_entity,artifact_entity
from Insurance.predictor import ModelResolver
import pandas as pd
from Insurance import utils
from Insurance import config
from sklearn.metrics import r2_score



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
            
            # find location of previous model
            transform_path = self.model_resolver.get_latest_tranformed_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            transform = utils.load_object(file_path=transform_path)
            model = utils.load_object(file_path=model_path)
            target_encoder = utils.load_object(file_path=target_encoder_path)

            #current model
            current_transform = utils.load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = utils.load_object(file_path=self.model_trainer_artifact.model_file_path)
            current_target_encoder = utils.load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            #compare previous model with current model
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[config.TARGET_COLUMN]
            y_true = target_df

            input_feature_name = list(transform.feature_names_in_)

            for i in input_feature_name:
                if test_df[i].dtype =='object':
                    test_df[i] = target_encoder.transform(test_df[i])
            input_arr = transform.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            previous_model_score = r2_score(y_true,y_pred)


            input_feature_name = list(current_transform.feature_names_in_)
            input_arr = current_transform.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)

            y_true = target_df
            current_model_score = r2_score(y_true,y_pred)


            #final comaprision betwwen both models
            if current_model_score <= previous_model_score:
                logging.info(f"Model is not better than previous model. Current model score: {current_model_score}, Previous model score: {previous_model_score}")
                raise Exception("Model is not better than previous model. Current model score: {current_model_score}, Previous model score: {previous_model_score}")
            model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                                improved_accuracy=current_model_score - previous_model_score)
            
            return model_evaluation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
        
