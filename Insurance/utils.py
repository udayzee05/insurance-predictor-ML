import pandas as pd
import numpy as np
import os
import sys
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import logging
import yaml
import dill

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from mongodb database  {database_name} and collection :  {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"find columns: {df.columns}")

        if "_id" in df.columns:
            logging.info(f"Dropping _id column")
            df.drop("_id", axis=1, inplace=True)
        logging.info(f"Shape of dataframe: {df.shape}")
        return df

    except Exception as e:
        raise InsuranceException(e, sys)

def write_yaml_file(file_path:str,data:dict)->None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as f:
            yaml.dump(data,f)
    except Exception as e:
        raise InsuranceException(e, sys)
    

def convert_columns_float(df:pd.DataFrame, exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtype != 'O':
                    df[column] = df[column].astype(float)
                    
        return df
    except Exception as e:
        raise InsuranceException(e, sys)



def save_object(file_path:str,obj:object)->None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as f:
            dill.dump(obj,f)
    except Exception as e:
        raise InsuranceException(e, sys)
    
def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file {file_path} does not exist")
        with open(file_path,"rb") as f:
            return dill.load(f)
    except Exception as e:
        raise InsuranceException(e, sys)