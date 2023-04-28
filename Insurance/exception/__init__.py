import os
import sys

class InsuranceException(Exception):
    def __init__(self, error_message:Exception, error_details:sys) -> None:
        super().__init__(error_message)
        self.error_message = InsuranceException.get_error_message(error_message, error_details=error_details)

    @staticmethod
    def get_error_message(error:Exception, error_details:sys) -> str:
        _,_ ,exc_tb = error_details.exc_info()
        line_number = exc_tb.tb_frame.f_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = f" Error occured python script name{file_name}" f"line_number{line_number}  error message {error}"

        return error_message

    def __str__(self) -> str:
        return InsuranceException.__name__.__str__()
