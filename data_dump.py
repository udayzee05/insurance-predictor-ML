import pandas as pd
import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://udayzee05:admin123@cluster0.pb2cada.mongodb.net/?retryWrites=true&w=majority")

DATA_FILE_PATH = "E:\Projects\\insurance-predictor-ML\\insurance.csv"
DATABASE_NAME = "INSURANCE"
COLLECTION_NAME = "INSURANCE_PROJECT"


if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns : {df.shape}")
    df.reset_index(drop=True, inplace = True )
    json_record = list(json.loads(df.T.to_json()).values())
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
