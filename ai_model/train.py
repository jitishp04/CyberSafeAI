from ai_model.utils.data_loader import load_data
from ai_model.utils.data_preprocessing import preprocess_text
from ai_model.utils.data_spilter import split_data
from ai_model.utils.training import train_model
from ai_model.utils.evaluation import evaluate_model
from ai_model.utils.model_save import save_and_version_model
from ai_model.utils.combine_data import combine_data
from backend.config.logger import logger
import os
from backend.config.config import MODEL_NAME, BASE_DIR, MODEL_REPO_URL

def train_and_evaluate_model():
    """
    Main training and evaluation pipeline.
    """
    logger.info("Starting training and evaluation pipeline...")

    try:
        # Step 1: Combine the data from different sources
        logger.info("Combining the data sources...")
        combine_data()
        
        # Step 2: Paths for raw and processed data
        raw_data_file = os.path.join(BASE_DIR, "data", "raw", "content_moderation_data.csv")

        # Step 3: Split raw data into training and testing sets
        logger.info("Splitting raw data into training and testing datasets...")
        train_file, test_file = split_data(raw_data_file)

        # Load and preprocess training data
        logger.info("Loading and preprocessing training data...")
        train_data = load_data(is_train=True)
        train_data["comment_text"] = train_data["comment_text"].apply(preprocess_text)
        
        # Create binary label column
        train_data["label"] = train_data[["toxic", "severe_toxic", "obscene", "threat", 
                                        "insult", "identity_hate"]].max(axis=1)
        train_data = train_data.reset_index(drop=True)

        # Train the model
        logger.info("Training the model...")
        model, tokenizer = train_model(train_data, MODEL_NAME)

        # Load and preprocess testing data
        logger.info("Loading and preprocessing testing data...")
        test_data = load_data(is_train=False)
        test_data["comment_text"] = test_data["comment_text"].apply(preprocess_text)
        test_data["label"] = test_data[["toxic", "severe_toxic", "obscene", "threat", 
                                      "insult", "identity_hate"]].max(axis=1)
        test_data = test_data.reset_index(drop=True)

        # Evaluate the model
        logger.info("Evaluating the model...")
        performance_metrics = evaluate_model(model, tokenizer, test_data)
        
        # Save and version both model and metrics
        models_dir = os.path.join(BASE_DIR, "models")
        logger.info(f"Dir, {models_dir}")
        model_dir, metrics_file = save_and_version_model(
            model=model,
            tokenizer=tokenizer,
            models_dir=models_dir,
            metrics=performance_metrics,
            repo_url=MODEL_REPO_URL
        )

        logger.info(f"Data after saving: {metrics_file}")
            
        logger.info("Training and evaluation completed.")
        logger.info(f"Model saved to: {model_dir}")
        logger.info(f"Metrics saved to: {metrics_file}")
        logger.info(f"Performance metrics: {performance_metrics}")
        
        return {
            'model': model,
            'metrics': performance_metrics,
            'success': True
        }

    except Exception as e:
        logger.error(f"Training failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    train_and_evaluate_model()