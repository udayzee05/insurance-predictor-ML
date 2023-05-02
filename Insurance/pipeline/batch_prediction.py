from Insurance.exception import InsuranceException
from Insurance.logger import logging
import numpy as np
import pandas as pd
import os
import sys
from Insurance import utils
from Insurance.predictor import ModelResolver
from datetime import datetime

PREDICTION_DIR = "prediction"
def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"batch prediction")
        model_resolver = ModelResolver(model_registry='saved_models')
        # Data loading
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)
       
        # Data Validation
        transform = utils.load_object(file_path=model_resolver.get_latest_tranformed_path())
        target_encoder = utils.load_object(file_path=model_resolver.get_latest_target_encoder_path())
        input_feature_names = list(transform.feature_names_in_)
    
        for i in input_feature_names:
            if df[i].dtypes == 'object':
                df[i] =target_encoder.fit_transform(df[i])

        input_arr = transform.transform(df[input_feature_names])
        model = utils.load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        df['prediction'] = prediction

        prediction_file_name = os.path.basename(input_file_path).replace('.csv',f'{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv')
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        logging.info(f"Batch prediction ended")
        return prediction_file_path

    except Exception as e:
        raise InsuranceException(e, sys)
    
