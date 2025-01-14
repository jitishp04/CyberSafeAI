# Import necessary modules and classes
from django.db import models

# Define the Admin model for the CSA_AdminApp application
class Admin(models.Model):
    email = models.EmailField(unique=True) # Email field with unique contraint
    password = models.CharField(max_length=128) 

    class Meta:
        app_label = 'CSA_AdminApp'  # Explicitly set the app_label
        # db_table = 'CSA_AdminApp_admin'
    
    # String representation of the model instance
    def __str__(self):
        return self.email
