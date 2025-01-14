# Import necessary modules and classes
from ai_model.train import train_and_evaluate_model
from backend.config.logger import logger

# Define a service class for managing AI model-related operations
class AIModelService:
    @staticmethod
    def train_model():
        try:
            result = train_and_evaluate_model()
            if result['success']:
                logger.info(f"Training completed successfully with metrics: {result['metrics']}")
                return result['metrics']
            raise Exception(result.get('error', 'Unknown error'))
        except Exception as e:
            logger.error(f"Training failed: {e}")# Log and re-raise any errors that occur during training
            raise
