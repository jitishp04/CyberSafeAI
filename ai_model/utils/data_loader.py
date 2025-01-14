import pandas as pd
from backend.config.logger import logger
from backend.config.config import TRAIN_DATA_PATH, TEST_DATA_PATH

def load_data(is_train=True):
    file_path = TRAIN_DATA_PATH if is_train else TEST_DATA_PATH
    try:
        logger.info(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        if data.empty:
            raise ValueError(f"The dataset at {file_path} is empty.")
        logger.info(f"Data loaded successfully")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        return None
