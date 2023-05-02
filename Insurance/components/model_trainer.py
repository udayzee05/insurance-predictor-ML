
import sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity import config_entity,artifact_entity
from sklearn.linear_model import LinearRegression
from Insurance import utils
from sklearn.metrics import r2_score


class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
            

    def train_model(self,X,y):
        try:
            lr = LinearRegression()
            lr.fit(X,y)
            return lr
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"{'>>'*5} Model Training {'<<'*5}")
            train_arr = utils.load_numpy_array_data(self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array_data(self.data_transformation_artifact.transform_test_path)
            X_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            model = self.train_model(X_train,y_train)
            y_hat_train = model.predict(X_train)
            r2_score_train = r2_score(y_train,y_hat_train)

            y_hat_test = model.predict(X_test)
            r2_score_test = r2_score(y_test,y_hat_test)

            if r2_score_test < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good enough, expected score is {self.model_trainer_config.expected_score} and actual score is {r2_score_test}")
            
            diff = abs(r2_score_train - r2_score_test)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model is overfitting, expected score is {self.model_trainer_config.expected_score} and actual score is {r2_score_test}")            
            
            utils.save_object(self.model_trainer_config.model_file_path,model)

            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_file_path=self.model_trainer_config.model_file_path,
                                                                          r2_score_train = r2_score_train,r2_score_test = r2_score_test)
            
            return model_trainer_artifact

        except Exception as e:
            raise InsuranceException(e, sys)