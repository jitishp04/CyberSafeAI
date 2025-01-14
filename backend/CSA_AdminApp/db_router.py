# Import necessary modules and classes
import logging
logging.basicConfig(level=logging.DEBUG) # Configure logging to display debug messages
from django.conf import settings # Import settings for custom configurations

class AdminDbRouter:
    def db_for_read(self, model, **hints):
        """
        Determine the database to use for read operations for a given model.
        """
        #logging.debug(f"db_for_read called for {model.__name__} from app {model._meta.app_label}")
        if model._meta.app_label == 'CSA_AdminApp' and model.__name__ == 'Admin':
            logging.debug("Using admin_db")
            return 'admin_db' # Use 'admin_db' for read operations for Admin model
        return 'default' # Default database for other models

    def db_for_write(self, model, **hints):
        """
        Determine the database to use for write operations for a given model.
        """
        #logging.debug(f"db_for_write called for {model.__name__} from app {model._meta.app_label}")
        if model._meta.app_label == 'CSA_AdminApp' and model.__name__ == 'Admin':
            logging.debug("Using admin_db")
            return 'admin_db' # Use 'admin_db' for write operations for Admin model
        return 'default' # Default database for other models

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects from any database.
        """
        #logging.debug(f"allow_relation called between {obj1.__class__.__name__} and {obj2.__class__.__name__}")
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine whether migrations are allowed on a specific database.
        """
        #logging.debug(f"allow_migrate called: db={db}, app_label={app_label}, model_name={model_name}")
        if settings.TESTING: # Allow all migrations during testing
            #logging.debug("TESTING is True. Allowing all migrations.")
            return True
        if app_label == 'CSA_AdminApp':
            logging.debug("Using admin_db")
            return db == 'admin_db' # Use 'admin_db' for CSA_AdminApp migrations
        return db == 'default' # Use default database for other migrations