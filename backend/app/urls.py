# Import necessary modules and classes
from django.urls import path
from app import views

# URL patterns for the app
urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_text, name='analyze_text'),
]
