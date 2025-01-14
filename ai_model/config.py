import datetime as datetime

import os

# Model Configuration
MODEL_NAME = "bert-base-uncased" # Use base BERT model
MAX_LEN = 128 # MAX_LEN of the input tokens
BATCH_SIZE = 32 # Number of samples in each training batch

#Training Configuration
LEARNING_RATE = 2e-5 # Step size for the weight model
EPOCHS = 3 # Number of times the model will be trained on the entire training data

# Data Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', 'content_moderation_data.csv')
TRAIN_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'train_data.csv')
TEST_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'test_data.csv')

# Output Configuration
MODEL_SAVE_PATH = "models/content_moderation_model.pth" # Path to save the trained model

#Logging Configuration
LOG_FILE = f"ai_model_{datetime.datetime.now().strftime('%Y%m%d')}.log"