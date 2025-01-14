# Import necessary modules and classes
from functools import cache
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .models import Admin
from app.models import TextAnalysis
from django.http import HttpResponse
from django.db.models import Q
import uuid
import csv
import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .services import AIModelService
from django.http import JsonResponse
from django.core.cache import cache
from config.model_manager import ModelManager
from config.config import MODEL_REPO_URL
from ai_model.utils.model_save import pull_repo
from pathlib import Path



# Global variable to track training status
BASE_DIR = Path(__file__).resolve().parent.parent
training_in_progress =  False
models_dir = BASE_DIR / "models"
pull_repo(models_dir ,MODEL_REPO_URL)

# Train the AI Model
class TrainModelView(APIView):
    def post(self, request):
        """API endpoint to trigger model training."""
        global training_in_progress
        try:
            training_in_progress = True
            metrics = AIModelService.train_model()
            training_in_progress = False
            return Response(
                {"message": "Model trained successfully", "metrics": metrics},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            training_in_progress = False
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def check_training_status(request):
    """Check if model training is currently in progress."""
    global training_in_progress
    return JsonResponse({
        'is_training': training_in_progress
    })

# Get model version view
def get_model_versions(request):
    """Retrieve all available AI model versions."""
    versions = ModelManager.get_available_versions()
    return JsonResponse({'versions': versions})

def change_model_version(request):
    """Change the current AI model version."""
    if request.method == 'POST':
        version = request.POST.get('version')
        if version in ModelManager.get_available_versions():
            ModelManager.set_current_version(version)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_current_model_version(request):
    """Retrieve the current AI model version."""
    current_version = ModelManager.get_current_version()
    return JsonResponse({'version': current_version})

# Admin login view
def admin_login(request):
    """Authenticate admin and establish a session."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(f"Email: {email}, Password: {password}")

        try:
            admin = Admin.objects.using('admin_db').get(email=email)
            #print(admin.password)
            if password == admin.password:
                token = str(uuid.uuid4())
                request.session['admin-token'] = token
                return redirect('dashboard')
            else:
                messages.error(request, "Incorrect email or password")
        except Admin.DoesNotExist:
            messages.error(request, "Admin with this email does not exist.")

    return render(request, 'CSA_AdminApp/admin_login.html', {})

# Dashboard view
def dashboard(request):
    if 'admin-token' not in request.session:
        return redirect('admin_login')

    #print(request.session.items())
    # Handle search query
    search_query = request.GET.get('q', '')  # Default to empty string

    # Get filter parameters from the request
    filters = {
        'toxic': request.GET.get('toxic', 'all'),
        'severe_toxic': request.GET.get('severe_toxic', 'all'),
        'obscene': request.GET.get('obscene', 'all'),
        'threat': request.GET.get('threat', 'all'),
        'insult': request.GET.get('insult', 'all'),
        'identity_hate': request.GET.get('identity_hate', 'all'),
    }

    # Start with all data or filter by search query
    data = TextAnalysis.objects.using('default').all()
    if search_query:
        data = data.filter(Q(text__icontains=search_query))

    # Apply filters dynamically
    for label, value in filters.items():
        if value == 'yes':
            data = data.filter(**{label: True})
        elif value == 'no':
            data = data.filter(**{label: False})

    # Pass the filter states and search query to the template
    context = {
        'data': data,
        'search_query': search_query,
        'toxic_filter': filters['toxic'],
        'severe_toxic_filter': filters['severe_toxic'],
        'obscene_filter': filters['obscene'],
        'threat_filter': filters['threat'],
        'insult_filter': filters['insult'],
        'identity_hate_filter': filters['identity_hate'],
    }

    return render(request, 'CSA_AdminApp/admin_dashboard.html', context)

# Export to CSV view
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="text_analysis_data.csv"'
    writer = csv.writer(response)
    
    # Write header matching the example format
    writer.writerow(['id', 'comment_text', 'toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'])
    
    # Get all entries and write rows
    for entry in TextAnalysis.objects.using('default').all():
        writer.writerow([
            entry.id,
            entry.text,
            int(entry.toxic),
            int(entry.severe_toxic),
            int(entry.obscene),
            int(entry.threat),
            int(entry.insult),
            int(entry.identity_hate)
        ])
    
    return response

# Upload CSV view
def upload_csv(request):
    """Upload and process a CSV file."""
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'No file was uploaded.')
            return redirect('dashboard')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'The uploaded file must be a CSV.')
            return redirect('dashboard')

        try:
            # Get the base directory path (go up one level from current directory)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Construct the path to the upload_data folder
            upload_dir = os.path.join(base_dir, 'data', 'upload_data')
            
            # Create the upload_data directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)
            
            # Set the file path with a fixed filename (will overwrite if exists)
            file_path = os.path.join(upload_dir, 'analysis_data.csv')
            
            # Save the uploaded file to the specified path
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            messages.success(request, 'CSV file uploaded and data imported successfully!')
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

    return redirect('dashboard')

# Delete selected texts view
def delete_texts(request):
    """Delete selected text analysis entries."""
    if request.method == 'POST':
        delete_ids = request.POST.getlist('delete_ids')
        if delete_ids:
            try:
                TextAnalysis.objects.using('default').filter(id__in=delete_ids).delete()
                messages.success(request, 'Selected entries were deleted successfully.')
            except Exception as e:
                messages.error(request, f"Error deleting entries: {e}")
        else:
            messages.error(request, 'No entries were selected for deletion.')
    return redirect('dashboard')

# Admin logout view
def admin_logout(request):
    """Log out the admin and clear the session."""
    if 'admin-token' in request.session:
        del request.session['admin-token']
    return redirect('admin_login')
