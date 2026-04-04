import sys
from networksecurity.logging.logger import logger  # import global logger


def error_message_detail(error, error_detail: sys):
    """Return detailed error message with file name and line number"""
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    return f"Error occurred in script: [{file_name}] at line: [{line_number}] error message: [{str(error)}]"


class CustomException(Exception):
    """Custom exception class with logging support"""

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)

        # generate detailed error message
        self.error_message = error_message_detail(error_message, error_detail)

        # log error automatically
        logger.error(self.error_message)

if __name__ == "__main__":
    import sys
    try:
        a = 10 / 0
    except Exception as e:
        raise CustomException(e, sys)