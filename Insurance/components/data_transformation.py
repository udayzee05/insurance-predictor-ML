
import os
import sys
import pandas as pd
import numpy as np
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity import config_entity,artifact_entity
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from Insurance.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from Insurance import utils


class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e, sys)

    @classmethod
    def get_data_transform_object(cls)-> Pipeline:
        try:
             
            pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
                ('scaler', RobustScaler())
            ])
   
            return pipeline
        except Exception as e:
            raise InsuranceException(e, sys)

    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            logging.info(f"{'>>'*5} Data Transformation {'<<'*5}")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df = train_df.drop([TARGET_COLUMN],axis=1) 
            input_feature_test_df = test_df.drop([TARGET_COLUMN],axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            label_encoder = LabelEncoder()
            target_feature_train_arr = target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()
            
            for col in input_feature_train_df.columns:
                if input_feature_train_df[col].dtype == 'O':
                    input_feature_train_df[col] = label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col] = label_encoder.transform(input_feature_test_df[col])

                else:
                    input_feature_train_df[col] = input_feature_train_df[col]
                    input_feature_test_df[col] = input_feature_test_df[col]

            transformation_pipeline = DataTransformation.get_data_transform_object()
            transformation_pipeline.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_train_path,array = train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_test_path,array = test_arr)

            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
                              obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
                              obj=label_encoder)      
              
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transform_train_path=self.data_transformation_config.transform_train_path,
                transform_test_path=self.data_transformation_config.transform_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)