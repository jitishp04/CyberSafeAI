from transformers import BertTokenizer
##from backend.logger import logger uncomment it if needed to log the usage of the utility function
import re

def preprocess_text(text):
    text = text.lower() # Convert text to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove mentions
    text = re.sub(r"#\w+", "", text)  # Remove hashtags
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabetic characters
    return text
