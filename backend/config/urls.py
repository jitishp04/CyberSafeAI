# Import necessary modules and classes
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('CSA_AdminApp.urls')),  # Change from 'backend.CSA_AdminApp.urls' to 'CSA_AdminApp.urls'
    path('', include('app.urls')),  # Change from 'backend.app.urls' to 'app.urls'
    path('', include('CSA_AdminApp.urls')),  # Include CSA_AdminApp's URLs
]
