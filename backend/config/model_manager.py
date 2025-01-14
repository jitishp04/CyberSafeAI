# Import necessary modules and classes
from django.core.cache import cache
import os

class ModelManager:
    DEFAULT_VERSION = 'trained_model_v1.0.0'

    @staticmethod
    def get_current_version():
        """Get the currently selected model version from cache"""
        return cache.get('current_model_version', ModelManager.DEFAULT_VERSION)

    @staticmethod
    def set_current_version(version):
        """Set the current model version in cache"""
        cache.set('current_model_version', version)

    @staticmethod
    def get_model_path():
        """Get the full path to the current model version."""
        current_version = ModelManager.get_current_version()
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models", 
            f"{current_version}" 
        )
        return model_path

    @staticmethod
    def get_available_versions():
        """Get list of available model versions"""
        models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
        versions = [d for d in os.listdir(models_dir) 
                   if os.path.isdir(os.path.join(models_dir, d)) and d.startswith('trained_model')]
        return sorted(versions, reverse=True)