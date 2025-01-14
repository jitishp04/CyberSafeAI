import pandas as pd
from backend.config.logger import logger
from backend.config.config import RAW_DATA_PATH, UPLOADED_DATA_PATH
import os

def combine_data(input_file=RAW_DATA_PATH, input_file2=UPLOADED_DATA_PATH, output_file=RAW_DATA_PATH):
    """
    Appends the uploaded data to the raw data file.

    Args:
        input_file (str): Path to the raw data file (base dataset)
        input_file2 (str): Path to the uploaded data file (new data to append)
        output_file (str): Path to save the combined data
    """
    logger.info("Starting data appending process...")

    try:
        # Load the raw data
        if os.path.exists(input_file):
            df1 = pd.read_csv(input_file)
            logger.info(f"Successfully loaded raw data with {len(df1)} rows")
        else:
            logger.error(f"Raw data file not found at {input_file}")
            return None

        # Load the uploaded data
        if os.path.exists(input_file2):
            df2 = pd.read_csv(input_file2)
            logger.info(f"Successfully loaded uploaded data with {len(df2)} rows")
        else:
            logger.error(f"Uploaded data file not found at {input_file2}")
            return None

        # Check for existing comment_text in raw data to avoid duplicates
        initial_upload_rows = len(df2)
        df2 = df2[~df2['comment_text'].isin(df1['comment_text'])]
        skipped_rows = initial_upload_rows - len(df2)
        
        if skipped_rows > 0:
            logger.info(f"Skipped {skipped_rows} duplicate rows from uploaded data")

        # Append new data to raw data
        combined_df = pd.concat([df1, df2], ignore_index=True)
        logger.info(f"Successfully combined data. Final dataset has {len(combined_df)} rows")

        # Save the combined data back to raw data file
        combined_df.to_csv(output_file, index=False)
        logger.info(f"Successfully saved combined data to {output_file}")

        return combined_df

    except Exception as e:
        logger.error(f"Error during data combining: {e}")
        raise

if __name__ == "__main__":
    combine_data()