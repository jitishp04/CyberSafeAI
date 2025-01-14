## Backend Folder

The **backend** folder contains the main Django app, including the models, views, URL routing, and business logic. It is responsible for handling HTTP requests, serving APIs, managing user data, and interacting with the AI model for content analysis.

### Contents:

- **/CSA_AdminApp**: The Django application for Admin that includes:
  - /migrations : Folder to make migrations into.
  - `apps.py`: Configures the CSA_AdminApp application settings.
  - `db_router.py`: Defines a database router to manage read/write operations and migrations for the Admin model, segregating it to the admin_db database.
  - `models.py`: Defines the Admin model for managing admin user data, including unique email and password fields, in the CSA_AdminApp application.
  - `services.py`: Provides the AIModelService class to manage AI model operations, including training and logging performance metrics.
  - `tests.py`: Discovers and loads all unit tests in the tests/ directory for execution.
  - `urls.py`: Defines URL patterns for admin authentication, dashboard operations, CSV management, text deletion, and machine learning model management.
  - `views.py`: Implements views for admin authentication, dashboard management, CSV import/export, AI model operations, and text analysis filtering, providing the core logic for the application's functionality.

- **/app**: The main Django application that includes:
  - /migrations : Folder to make migrations into.
  - `admin.py`: Customizes the Django admin interface for managing TextAnalysis entries.
  - `apps.py`: Configures the Django app settings.
  - `models.py`: Defines the Django model for the TextAnalysis database table.
  - `urls.py`: URL configuration for routing URLs to corresponding views.
  - `views.py`: Views that handle user requests and render templates.

- **/config**: Configuration files for the Django project.
  - /staticfiles : Folder to move static files into.
  - `asgi.py`: Configures ASGI for the project, enabling asynchronous server communication.
  - `config.py`: Centralizes application configurations, including model, training, data paths, and logging settings.
  - `logger.py`: Sets up a custom logger to log application events to the console and daily log files.
  - `model_manager.py`: Manages model versions, paths, and caching for the application.
  - `settings.py`: The main settings file that configures the project (e.g., database, security, middleware).
  - `urls.py`: The main URL routing configuration.
  - `wsgi.py`: Entry point for deploying the Django application in production.

- **/data**: Data files for the Django project.
  - /processed : Folder to house processed data files. 
    - `test_data.csv`: CSV file with testing data.
    - `train_data.csv`: CSV file with training data.
  - /raw : Folder to house raw data files.
    - `content_moderation_data.csv`: CSV file with unprocessed data.

- **/models**: The folder that houses each model as it is trained.

- **/tests**: The main Django application that includes:
  - /migrations : Folder to make migrations into.
  - `test_model.py`: Contains unit tests for the Admin and TextAnalysis models, ensuring proper creation, validation, default values, and database operations.
  - `test_view.py`: Contains unit tests for admin login, dashboard operations, model training, home view pagination, and text analysis functionalities.

- `requirements.txt`: Backend dependencies such as Django, Django Rest Framework, etc.
- `manage.py`: Django management script for running server, migrations, etc.

### Purpose:
This is the heart of the application, where the logic for content submission, moderation, and analysis happens. It handles user interactions, communicates with the database, and serves AI-powered analysis results.
