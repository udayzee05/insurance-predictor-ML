from Insurance.components import *
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os
from typing import Optional
import sys
from Insurance.entity.config_entity import *


class ModelResolver:
    def __init__(self,model_registry:str = 'saved_models',
                 transform_dir_name = "transform",
                 target_encoder_dir_name = "target_encoder",
                 model_dir_name = "model"):

        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transform_dir_name = transform_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name

        
    
    def get_latest_dir_path(self)-> Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)

            if len(dir_names) ==0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)

            return os.path.join(self.model_registry,f"{latest_dir_name}")

        except Exception as e:
            raise InsuranceException(e, sys)
        

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("No model found")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)

        except Exception as e:
            raise InsuranceException(e, sys)

    def get_latest_tranformed_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                raise Exception("Transformed data is not availabel")
            return os.path.join(latest_dir,self.transform_dir_name,TRANSFORM_OBJECT_FILE_NAME)

        except Exception as e:
            raise InsuranceException(e, sys)
        

    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Target encoder is not availabel")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise InsuranceException(e, sys)
    

    def get_latest_saved_dir_path(self)->str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num + 1}")
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_save_transform_path(self):
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir,self.transform_dir_name,TRANSFORM_OBJECT_FILE_NAME) # transform.pkl

        except Exception as e:
            raise InsuranceException(e, sys)
    

    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME) # encoder.pkl
        except Exception as e:
            raise InsuranceException(e, sys)