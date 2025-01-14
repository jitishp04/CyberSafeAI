from utils.data_loader import load_data
from preprocessing.text_processor import preprocess_text
from utils.logger import Logger
#Load data from file
data = load_data("data/train_data.csv")

if data is not None:
    sample_text = data['comment_text'].iloc[0]

    processed_data = preprocess_text(sample_text)
else:
    Logger.error("Data not loaded")

Logger.info("Data processing test completed")