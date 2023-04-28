import os
from dataclasses import dataclass
from datetime import datetime
from Insurance.exception import InsuranceException
from Insurance.logger import logging

@dataclass
class DataIngestionArtifact:
    feature_store_filepath:str
    train_file_path:str
    test_file_path:str
