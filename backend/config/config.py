# Import necessary modules and classes
import datetime as datetime
import os
from backend.config.logger import logger

# Model Configuration
MODEL_NAME = "bert-base-uncased"  # Use base BERT model
MAX_LEN = 128  # MAX_LEN of the input tokens
BATCH_SIZE = 32  # Number of samples in each training batch

# Training Configuration
LEARNING_RATE = 2e-5  # Step size for the weight model
EPOCHS = 3  # Number of times the model will be trained on the entire training data

# Data Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Point to 'backend'
DATA_DIR = os.path.join(BASE_DIR, 'data')  # Correctly points to backend/data

# Model and Repository Configuration
MODEL_REPO_PATH = os.path.join(BASE_DIR, 'models')  # Path to model repository
METRICS_DIR = os.path.join(MODEL_REPO_PATH, 'metrics')    # Path to metrics directory
MODEL_REPO_URL = "https://github.com/cybersafeai/models"  # Replace with your repo URL
GIT_BRANCH = "main"  # Default branch name

# Data Paths
UPLOADED_DATA_PATH = os.path.join(DATA_DIR, 'upload_data', 'analysis_data.csv')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', 'content_moderation_data.csv')
TRAIN_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'train_data.csv')
TEST_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'test_data.csv')

# Ensure necessary directories exist
def create_dirs_if_not_exist():
    directories = [
        DATA_DIR,                    # backend/data
        os.path.join(DATA_DIR, 'raw'),       # backend/data/raw
        os.path.join(DATA_DIR, 'processed'), # backend/data/processed              # metrics directory
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Directory created: {directory}")
        else:
            logger.debug(f"Directory already exists: {directory}")

# Output Configuration
MODEL_SAVE_PATH = os.path.join(MODEL_REPO_PATH, "content_moderation_model.pth")  # Path to save the trained model

# Logging Configuration
LOG_FILE = os.path.join(BASE_DIR, '..', f"ai_model_{datetime.datetime.now().strftime('%Y%m%d')}.log")  # Logging path

# Call function to ensure directories exist
create_dirs_if_not_exist()