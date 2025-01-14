# Import necessary modules and classes
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from unittest.mock import patch,Mock
from django.urls import reverse
from app.models import TextAnalysis
from app.views import analyze_text
from django.contrib.messages import get_messages
from CSA_AdminApp.services import AIModelService
from django.utils import timezone
from CSA_AdminApp.models import Admin
from django.test.client import Client
import torch
import os
import tempfile
import csv

# Tests for Admin Login and Authentication
class AdminLoginViewTests(TestCase):
    databases = {'default', 'admin_db'}

    def setUp(self):
        """Set up the environment for admin login tests."""
        self.admin_user = Admin.objects.create(email='admin@example.com', password='testpassword')
        self.text_data = TextAnalysis.objects.create(
            text='This is a test',
            toxic=True,
            obscene=False,
            insult=True,
            created_at=timezone.now()
        )
        self.client = Client()

    def test_admin_login_success(self):
        """Test successful admin login."""
        response = self.client.post(reverse('admin_login'), {
            'email': 'admin@example.com',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertIn('admin-token', self.client.session)

    def test_admin_login_failed(self):
        """Test failed admin login with incorrect credentials."""
        response = self.client.post(reverse('admin_login'),{
            'email': 'admin@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), "Incorrect email or password")
    
    def test_dashboard_view_logged_in(self):
        """Test accessing dashboard when logged in."""
        self.client.post(reverse('admin_login'), {
            'email': 'admin@example.com',
            'password': 'testpassword'
        })
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_not_logged_in(self):
        """Test accessing dashboard without logging in."""
        self.client.post(reverse('admin_login'), {
            'email': 'admin@example.com',
            'password': 'wrongpassword'
        })
        response = self.client.get(reverse('admin_login'))
        self.assertEqual(response.status_code, 200)


        
# Tests for Admin Dashboard Operations
class AdminDashboardViewTests(TestCase):
    databases = {'default', 'admin_db'}

    def setUp(self):
        # Set up the admin user
        self.admin_user = Admin.objects.create(email='admin@example.com', password='testpassword')
        self.text_data = TextAnalysis.objects.create(
            text='This is a test',
            toxic=True,
            obscene=False,
            insult=True,
            created_at=timezone.now()
        )
        self.client = Client()

        # Create a temporary file to store the CSV
        self.test_csv = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv')
        self.test_csv_name = self.test_csv.name  # Store the name for later deletion

        # Write the header and a row of data
        writer = csv.writer(self.test_csv)
        writer.writerow(['Text', 'Toxic','Severe Toxic','Obscene','Threat','Insult','Identity Hate','Created At'])
        # Ensure boolean fields are strings to match CSV reading logic
        writer.writerow(['Test text', '1', '0', '1', '1', '0', '0', timezone.now().isoformat()])
        self.test_csv.close()  # Close the file to allow it to be used in the test

    def tearDown(self):
        # Clean up the temporary CSV file
        if os.path.exists(self.test_csv_name):
            os.remove(self.test_csv_name)

    def test_export_csv(self):
        # Log in the admin user
        self.client.post(reverse('admin_login'), {
            'email': 'admin@example.com',
            'password': 'testpassword'
        })
        
        # Simulate exporting data to CSV
        response = self.client.get(reverse('export_to_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('text_analysis_data.csv', response['Content-Disposition'])

    def test_upload_csv(self):
        # Log in the admin user
        self.client.post(reverse('admin_login'), {
            'email': 'admin@example.com',
            'password': 'testpassword'
        })

        # Open the temporary CSV file for upload
        with open(self.test_csv_name, 'rb') as f:
            response = self.client.post(reverse('upload_csv'), {'csv_file': f})

        # Assert the response redirects to the dashboard
        self.assertRedirects(response, reverse('dashboard'))

        # Get the messages from the response after the redirect
        messages = list(get_messages(response.wsgi_request))

        # Assert that there is a message indicating success
        self.assertGreater(len(messages), 0)  # Ensure there is at least one message
        self.assertEqual(str(messages[0]), 'CSV file uploaded and data imported successfully!')

        # Optionally, check if the data was actually imported
        self.assertEqual(TextAnalysis.objects.count(), 1) 

    def test_delete_text(self):
        # Log in the admin user
        self.client.post(reverse('admin_login'), {
            'email': 'admin@example.com',
            'password': 'testpassword'
        })

        # Simulate deleting the text
        response = self.client.post(reverse('delete_texts'), {'delete_ids': [self.text_data.id]})
        self.assertRedirects(response, reverse('dashboard'))

        # Assert that the text was deleted
        self.assertEqual(TextAnalysis.objects.count(), 0)

# Tests for Training Model
class TrainModelViewTests(TestCase):
    databases = {'default', 'admin_db'}
    def setUp(self):
        """Set up the environment for training model tests."""
        self.client = APIClient()

    @patch('CSA_AdminApp.views.AIModelService.train_model', return_value={'accuracy': 0.95})
    def test_train_model_success(self, mock_train_model):
        """Test successful training of the model."""
        url = reverse('train-model') 
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Model trained successfully", response.data["message"])
        self.assertIn("accuracy", response.data["metrics"])
   
    @patch('CSA_AdminApp.views.AIModelService.train_model', side_effect=Exception("Training failed"))
    def test_train_model_failure(self, mock_train_model):
        """Test failed model training."""
        url = reverse('train-model')  
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Training failed")

# Tests for Home View Pagination and Filtering
class ModHomeViewTest(TestCase):
    def setUp(self):
        for i in range(25):
            TextAnalysis.objects.create(
                text=f"Sample text {i}",
                toxic=False,
                toxic_probability=0.1,
                severe_toxic=False,
                severe_toxic_probability=0.05,
                obscene=False,
                obscene_probability=0.1,
                threat=False,
                threat_probability=0.1,
                insult=False,
                insult_probability=0.1,
                identity_hate=False,
                identity_hate_probability=0.1
            )    
    def test_home_page_loads(self):
        """Test that the home page loads correctly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moderation/home.html")

    def test_home_page_filter_toxic(self):
        """Test filtering functionality for toxic entries."""
        response = self.client.get(reverse('home') + '?filter=toxic')
        self.assertEqual(response.status_code, 200)
        self.assertIn("analyses", response.context)

    def test_home_page_pagination(self):
        """Test pagination functionality on the home page."""
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['analyses']), 10)

# class AnalyzeTextViewTests(TestCase):
#     @patch('app.views.BertTokenizerFast.from_pretrained')
#     @patch('app.views.BertForSequenceClassification.from_pretrained')
#     def test_analyze_text(self, mock_model, mock_tokenizer):
#         # Define the model path to simulate
#         mock_model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "trained_model_v1.0.0")
        
#         # Mock the tokenizer and model behavior
#         mock_tokenizer_instance = mock_tokenizer.return_value
#         mock_model_instance = mock_model.return_value

#         # Mock tokenizer's behavior (what it returns when called)
#         mock_tokenizer_instance.return_value = {'input_ids': torch.tensor([[101, 102]])}
        
#         # Mock model's behavior (what it returns when called)
#         mock_model_instance.return_value = torch.nn.Module()  # Just a simple placeholder
#         mock_model_instance.forward = patch('torch.nn.Module.forward').start()
#         mock_model_instance.forward.return_value.logits = torch.tensor([[0.1, 0.9]])

#         # Simulate the path being passed into the from_pretrained method
#         mock_tokenizer.from_pretrained = patch('transformers.BertTokenizerFast.from_pretrained').start()
#         mock_model.from_pretrained = patch('transformers.BertForSequenceClassification.from_pretrained').start()
        
#         # Ensure the tokenizer and model are using the mocked path
#         mock_tokenizer.from_pretrained.assert_called_with(mock_model_path, local_files_only=True)
#         mock_model.from_pretrained.assert_called_with(mock_model_path, local_files_only=True)

#         # Make a POST request with the text you want to analyze
#         response = self.client.post('/analyze/', {'text': 'test text'})

#         # Assert that the response is as expected
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('results', response.json())
#         self.assertIn('toxic', response.json()['results'])
#         self.assertIn('probability', response.json()['results']['toxic'])
    
#     @patch('app.views.vectorizer')
#     def test_analyze_text_no_text(self, mock_vectorizer):
#         response = self.client.post(self.url, {'text': ''})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['error'], 'No text provided')
    
#     @patch('app.views.vectorizer')
#     @patch('app.views.models', new_callable=dict)
#     def test_analyze_text_model_not_loaded(self, mock_models, mock_vectorizer):
#         # Simulate that models are not loaded properly
#         mock_vectorizer.transform.return_value = [1]
#         response = self.client.post(self.url, {'text': 'This is a test text'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['error'], 'Model not loaded properly')
    
#     @patch('app.views.vectorizer')
#     @patch('app.views.models')
#     def test_analyze_text_error_handling(self, mock_models, mock_vectorizer):
#         # Simulate an error during text analysis
#         mock_vectorizer.transform.side_effect = Exception('Vectorization error')
        
#         response = self.client.post(self.url, {'text': 'This is a test text'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('error', response.json())
#         self.assertEqual(response.json()['error'], 'Error analyzing text: Vectorization error')
