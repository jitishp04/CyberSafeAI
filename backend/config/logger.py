# Import necessary modules and classes
import logging
import os
import datetime

def setup_logger():
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate the log filename based on today's date (e.g., 'ai_model_20241202.log')
    log_filename = f"ai_model_{datetime.datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(log_dir, log_filename)

    # Create a custom logger
    logger = logging.getLogger('backend')
    logger.setLevel(logging.DEBUG)
    
    logger.propagate = False

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_filepath, encoding='utf-8')  # UTF-8 encoding for the log file
    c_handler.setLevel(logging.INFO)  # Set stream handler level to INFO
    f_handler.setLevel(logging.DEBUG)  # Set file handler level to DEBUG

    # Create formatters and add them to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # Add handlers to logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

# Create a global logger
logger = setup_logger()
