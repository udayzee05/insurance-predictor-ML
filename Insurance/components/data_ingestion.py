import os
import sys
import pandas as pd
import numpy as np
from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.entity import config_entity,artifact_entity
from Insurance import utils
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config: config_entity.DataIngestionConfig):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise InsuranceException(e, sys)
    
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"{'>>'*5} Export Collection data as dataframe {'<<'*5}")
            df = pd.DataFrame = utils.get_collection_as_dataframe(database_name=self.data_ingestion_config.database_name,
                                                               collection_name=self.data_ingestion_config.collection_name)
            # replace na with nan
            df.replace(to_replace="na",value=np.nan,inplace=True)


            # save data into feature store
            logging.info(f"{'>>'*5} Save data into feature store if not availabel {'<<'*5}")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_filepath)
            os.makedirs(feature_store_dir,exist_ok=True)
            
            logging.info(f"{'>>'*5} Save df to feature_store folder{'<<'*5}")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_filepath,index=True)

            logging.info(f"{'>>'*5} Split data into train and test {'<<'*5}")
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            logging.info(f"{'>>'*5} Create dataset dir folder if not exist {'<<'*5}")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info(f"{'>>'*5} Save train and test to dataset folder {'<<'*5}")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=True)

            # prepare artifact folder
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(feature_store_filepath=self.data_ingestion_config.feature_store_filepath,
                                                                            train_file_path=self.data_ingestion_config.train_file_path,
                                                                            test_file_path=self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e, sys)