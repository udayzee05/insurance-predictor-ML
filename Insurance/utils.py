import pandas as pd
import numpy as np
import os
import sys
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import logging

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
