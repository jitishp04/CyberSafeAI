import pandas as pd
from sklearn.model_selection import train_test_split
from backend.config.logger import logger
from backend.config.config import RAW_DATA_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH

def split_data(input_file=RAW_DATA_PATH, train_output=TRAIN_DATA_PATH, test_output=TEST_DATA_PATH, train_ratio=0.7, random_state=42):
    """
    Splits the data into training and testing sets and saves them to disk.

    Args:
        input_file (str): Path to the input data file.
        train_output (str): Path to save the training data.
        test_output (str): Path to save the testing data.
        train_ratio (float): Proportion of the data to use for training.
        random_state (int): Seed for reproducibility.

    Returns:
        str, str: Paths to the saved training and testing datasets.
    """
    logger.info("Starting data split process...")

    try:
        # Load the raw data
        df = pd.read_csv(input_file)

        # Split the data
        train_data, test_data = train_test_split(df, train_size=train_ratio, random_state=random_state)

        # Save the datasets
        train_data.to_csv(train_output, index=False)
        test_data.to_csv(test_output, index=False)

        logger.info(f"Data split completed successfully: {train_output}, {test_output}")
        return train_output, test_output

    except Exception as e:
        logger.error(f"Error during data split: {e}")
        raise

if __name__ == "__main__":
    split_data()
