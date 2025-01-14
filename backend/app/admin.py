# Import necessary modules and classes
from django.contrib import admin
from .models import TextAnalysis

@admin.register(TextAnalysis)
class TextAnalysisAdmin(admin.ModelAdmin):
    # Specify fields to display in the admin list view
    list_display = ('text', 'toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate', 'created_at')

    # Add filters to the admin interface for these fields
    list_filter = ('toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate', 'created_at')

    # Enable search functionality for the specified fields
    search_fields = ('text',)

    # Mark certain fields as read-only in the admin interface
    readonly_fields = ('created_at',)

    # Specify the default ordering of the model instances in the admin interface
    ordering = ('-created_at',)