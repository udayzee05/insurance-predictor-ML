from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os
import sys
from Insurance.utils import get_collection_as_dataframe
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity
# def test_logger_and_exception():
#     try:
#         logging.info("Start test_logger_and_exception")
#         result = 3/4
#         print(result)
#         logging.info("End test_logger_and_exception")
#     except Exception as e:
#         logging.debug(str(e))
#         raise InsuranceException(e, sys)
    


if __name__=="__main__":
    try:
        # test_logger_and_exception()
        #get_collection_as_dataframe(database_name="INSURANCE",collection_name="INSURANCE_PROJECT")
        logging.info(f"{'>>'*20} main function {'<<'*20}")
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
    except Exception as e:
        raise InsuranceException(e, sys)