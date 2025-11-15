import sys
from grow_trader.logging.logger import logger

class CustomException(Exception):
    def __init__(self, error_message:Exception, error_detail:sys):
        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name,self.lineno,str(self.error_message)
        )
    def __repr__(self):
        return CustomException.__name__.__str__()
if __name__ == "__main__":
    try:
        logger.info("The try block has started")
        a = 1/0
    except Exception as e:
        raise CustomException(e, sys)