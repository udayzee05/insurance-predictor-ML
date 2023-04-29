import os
import sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity import config_entity,artifact_entity
from Insurance.entity.config_entity import DataIngestionConfig
import pandas as pd
from typing import Optional
from scipy.stats import ks_2samp
import numpy as np
from Insurance import utils,config

class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,\
                 data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*5} Data Validation {'<<'*5}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise InsuranceException(e, sys)
    

    def drop_missing_values(self, df: pd.DataFrame, report_key_name: str) -> Optional[pd.DataFrame]:
        if df is None:
            return None
        
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isnull().sum() / df.shape[0]
            drop_columns_names = null_report[null_report >= threshold].index

            self.validation_error[report_key_name] = list(drop_columns_names)

            df.drop(columns=drop_columns_names, axis=1, inplace=True)
            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise InsuranceException(e, sys)



    def is_required_column_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df
            current_columns = set(current_df.columns)

            missing_columns =[]
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column {base_column} is missing in current dataframe")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns 
                return False
            return True
        except Exception as e:
            raise InsuranceException(e, sys)

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                if base_column in current_columns:
                    base_column_data = base_df[base_column]
                    current_column_data= current_df[base_column]
                    distribution = ks_2samp(base_column_data,current_column_data)
                    if distribution.pvalue > 0.05:
                        # Null hypothesis  accept
                        drift_report[base_column] = {
                            "p_value":float(distribution.pvalue),
                            "distribution":True}
                    else:
                        drift_report[base_column] = {
                            "p_value":float(distribution.pvalue),
                            "distribution":False
                        }
            self.validation_error[report_key_name] = drift_report

        except Exception as e:        
            raise InsuranceException(e, sys)
        

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"{'>>'*5} Data Validation reading base data {'<<'*5}")

            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df = base_df.replace("na", np.nan)
            base_df = self.drop_missing_values(df=base_df, report_key_name="Missing Values within base dataset")
            
            logging.info(f"{'>>'*5} Reading train data {'<<'*5}")

            train_df = pd.read_csv(self.data_ingestion_config.train_file_path)
            train_df = train_df.replace("na",np.nan)
            train_df = self.drop_missing_values(df = train_df,report_key_name="Missing Values within train dataset")
            
            logging.info(f"{'>>'*5} Reading test data {'<<'*5}")

            test_df = pd.read_csv(self.data_ingestion_config.train_file_path)            
            test_df = test_df.replace("na",np.nan)
            test_df = self.drop_missing_values(df = test_df,report_key_name="Missing Values within test dataset")
         
            exclude_columns = [config.TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)
           
            train_df_columns_status = self.is_required_column_exists(base_df=base_df,current_df=train_df,report_key_name="data drift within train dataset")
            test_df_columns_status = self.is_required_column_exists(base_df=base_df,current_df=test_df,report_key_name="data drift within test dataset")

            if train_df_columns_status :
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="Data Drift within train dataset")
            if test_df_columns_status:
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="Data Drift within test dataset")

            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            return data_validation_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)