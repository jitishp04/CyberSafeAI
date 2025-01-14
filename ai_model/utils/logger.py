import logging
import os
from config import LOG_FILE

def setup_logger(log_filename=LOG_FILE):
    ## Create a log file in the logs directory
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Cretae a cutom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Cretae formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)


    # Add handler to logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

# Create a global logger
logger = setup_logger()