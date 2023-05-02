from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os,sys
from Insurance.entity import artifact_entity,config_entity
from Insurance.predictor import ModelResolver
from Insurance import utils



class ModelPusher:
    def __init__(self,model_pusher_config:config_entity.ModelPusherConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise InsuranceException(e, sys)
    
    def initiate_model_pusher(self)->artifact_entity.ModelPusherArtifact:
        try:
            logging.info(f"{'>>' * 5}Model Pusher started.{'<<' * 5} ")
            transform  = utils.load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = utils.load_object(file_path=self.model_trainer_artifact.model_file_path)
            target_encoder = utils.load_object(file_path=self.data_transformation_artifact.target_encoder_path)


            # model pusher directory
            utils.save_object(file_path=self.model_pusher_config.pusher_transform_path,obj=transform)
            utils.save_object(file_path=self.model_pusher_config.pusher_model_path,obj=model)
            utils.save_object(file_path=self.model_pusher_config.pusher_target_encoder_path,obj=target_encoder)

            # save model

            transform_path = self.model_resolver.get_latest_save_transform_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            print(model_path)
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()
            
            utils.save_object(file_path=transform_path,obj=transform)
            utils.save_object(file_path=model_path,obj=model)
            utils.save_object(file_path=target_encoder_path,obj=target_encoder)

            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                                                                       saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher completed")
            return model_pusher_artifact 

        except Exception as e:
            raise InsuranceException(e, sys)