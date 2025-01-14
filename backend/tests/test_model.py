# Import necessary modules and classes
import logging
from django.test import TestCase, Client
from django.utils import timezone
from CSA_AdminApp.models import Admin
from app.models import TextAnalysis
from datetime import timedelta

# Test suite for the Admin model
class AdminTest(TestCase):
    databases = {'default','admin_db'}
    # Specify the databases used in these tests
    def test_admin_create(self):
        """Test the creation of an Admin model instance."""
        admin = Admin.objects.create(email='newadmin@example.com',password='newpass')
        self.assertEqual(admin.email,'newadmin@example.com')
        self.assertEqual(admin.password,'newpass')
        logging.debug("Model tests: Test create user: PASSED")
    
    def test_unique_admin_email(self):
        """Test that Admin email must be unique."""
        Admin.objects.create(email='test@example.com', password='securepassword123')
        with self.assertRaises(Exception):
            Admin.objects.create(email='test@example.com', password='anotherpassword')
        logging.debug("Model tests: Test unique email functionality: PASSED")

# Test suite for the TextAnalysis model
class TextAnalysisTest(TestCase):
    # Specify the databases used in these tests
    databases = {'default','admin_db'}
    
    """Set up mock data for TextAnalysis tests."""
    def setUp(self):
        self.text_analysis = TextAnalysis.objects.create(
            text="Die please",
            toxic=True,
            toxic_probability=0.85,
            obscene=False,
            obscene_probability=0.05,
            insult=True,
            insult_probability=0.90,
            created_at=timezone.now() - timedelta(days=1)  # Set a past date for testing
        )
    logging.debug("Model tests: Mock Text data created")
    
    def test_textAnalysis_create(self):
        """Test the creation of a TextAnalysis model instance."""
        self.assertEqual(self.text_analysis.text, "Die please")
        self.assertTrue(self.text_analysis.toxic)
        self.assertEqual(self.text_analysis.toxic_probability, 0.85)
        self.assertFalse(self.text_analysis.obscene) 
        self.assertEqual(self.text_analysis.obscene_probability, 0.05)
        self.assertTrue(self.text_analysis.insult)
        self.assertEqual(self.text_analysis.insult_probability, 0.90)
    logging.debug("Model tests: Test adding new analysed test to the database: PASSED")

    def test_default_values(self):
        """Test default values of a new TextAnalysis instance."""
        text_analysis_default = TextAnalysis.objects.create(text="Default test")
        self.assertFalse(text_analysis_default.toxic)  
        self.assertEqual(text_analysis_default.toxic_probability, 0.0)  
        self.assertFalse(text_analysis_default.obscene)  
        self.assertEqual(text_analysis_default.obscene_probability, 0.0) 
        self.assertFalse(text_analysis_default.insult) 
        self.assertEqual(text_analysis_default.insult_probability, 0.0)
    logging.debug("Model tests: Test check initial analysis values: PASSED")

    def test_created_at(self):
        """Test the created_at field to ensure it's set correctly."""
        new_text_analysis = TextAnalysis.objects.create(text="Created at test")
        self.assertTrue(isinstance(new_text_analysis.created_at, timezone.datetime))
        self.assertLess(new_text_analysis.created_at, timezone.now())
    logging.debug("Model tests: Test time of creation functionality: PASSED")

    def test_database_operations(self):
        """Test basic database operations."""
        text_analysis = TextAnalysis.objects.create(text="Another test entry")
        self.assertEqual(TextAnalysis.objects.count(), 2) 
        self.assertEqual(text_analysis.text, "Another test entry")
        text_analysis.delete()
        self.assertEqual(TextAnalysis.objects.count(), 1)
    logging.debug("Model tests: Test adding new analysis: PASSED")
