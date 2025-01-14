# Import necessary modules and classes
from django.db import models
from django.utils import timezone

# Define the TextAnalysis model to store text and its analysis results
class TextAnalysis(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    # Results fields
    toxic = models.BooleanField(default=False)
    toxic_probability = models.FloatField(default=0.0)
    severe_toxic = models.BooleanField(default=False)
    severe_toxic_probability = models.FloatField(default=0.0)
    obscene = models.BooleanField(default=False)
    obscene_probability = models.FloatField(default=0.0)
    threat = models.BooleanField(default=False)
    threat_probability = models.FloatField(default=0.0)
    insult = models.BooleanField(default=False)
    insult_probability = models.FloatField(default=0.0)
    identity_hate = models.BooleanField(default=False)
    identity_hate_probability = models.FloatField(default=0.0)

    # Meta class to define model-specific options    
    class Meta:
        db_table = 'moderation_textanalysis'
        #managed = False
        ordering = ['-created_at']
        verbose_name = 'Text Analysis'
        verbose_name_plural = 'Text Analyses'

    # Define how the model instance is represented as a string
    def __str__(self):
        return f"{self.text[:50]}... ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
