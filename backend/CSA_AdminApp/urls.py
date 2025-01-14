# Import necessary modules and classes
from django.urls import path
from . import views
from app.views import home
from .views import TrainModelView

# Define URL patterns for the app
urlpatterns = [
    # Admin login and logout views
    path("login/", views.admin_login, name="admin_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("", home, name="view_site"),

    # CSV-related functionality
    path("export_to_csv/", views.export_to_csv, name="export_to_csv"),
    path("upload_csv/", views.upload_csv, name="upload_csv"),
    
    # Delete texts view
    path("delete_texts/", views.delete_texts, name="delete_texts"),

    # Machine learning model management
    path("train/", TrainModelView.as_view(), name="train-model"),
    path("check-training/", views.check_training_status, name="check_training"),
    path("get-model-versions/", views.get_model_versions, name="get_model_versions"),
    path(
        "get-current-model-version/",
        views.get_current_model_version,
        name="get_current_model_version",
    ),
    path(
        "change-model-version/", views.change_model_version, name="change_model_version"
    ),
]
