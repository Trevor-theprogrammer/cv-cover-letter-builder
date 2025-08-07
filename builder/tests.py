from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CV, CoverLetter
from unittest.mock import patch, MagicMock

class BuilderViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Create a dummy CV instance. Adjust fields as necessary based on your CV model.
        self.cv = CV.objects.create(title="Test CV", user=self.user)
    
    def test_dashboard_view(self):
        # Verify that the dashboard view displays the created CV.
        response = self.client.get(reverse('builder:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cv.title)
    
    def test_create_cv_view_get(self):
        response = self.client.get(reverse('builder:create_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/create_cv.html')
    
    def test_create_cv_view_post(self):
        # Test POST request for creating a new CV.
        data = {'title': 'New CV'}  # Adjust according to the actual fields required by CVForm.
        response = self.client.post(reverse('builder:create_cv'), data)
        # Expect redirection upon successful creation.
        self.assertEqual(response.status_code, 302)
    
    def test_generate_cover_letter_view_get(self):
        response = self.client.get(reverse('builder:generate_cover_letter'))
        self.assertEqual(response.status_code, 200)
        # Updated template name based on current implementation
        self.assertTemplateUsed(response, 'builder/enhanced_ai_cover_letter.html')
    
    def test_ai_cover_letter_view_get(self):
        # Test the AI cover letter view
        response = self.client.get(reverse('builder:ai_cover_letter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/ai_cover_letter.html')
    
    def test_upload_cv_view_get(self):
        # Test the upload CV view
        response = self.client.get(reverse('builder:upload_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/upload_cv_analyzer.html')

class AIServicesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    @patch('builder.ai_services.OpenAI')
    def test_ai_service_initialization(self, mock_openai):
        # Test AI service initialization
        from .ai_services import EnhancedAICoverLetterService
        
        service = EnhancedAICoverLetterService()
        self.assertIsNotNone(service)
    
    def test_cv_insights_extraction_fallback(self):
        # Test CV insights extraction with fallback data
        from .ai_services import EnhancedAICoverLetterService
        
        service = EnhancedAICoverLetterService()
        test_cv = "John Doe, Software Engineer with 5 years experience in Python and Django."
        
        insights = service.extract_cv_insights(test_cv)
        
        self.assertIsInstance(insights, dict)
        self.assertIn('skills', insights)
        self.assertIn('experience', insights)
        self.assertIn('summary', insights)
    
    def test_comprehensive_cv_analysis_fallback(self):
        # Test comprehensive CV analysis with fallback data
        from .ai_services import EnhancedAICoverLetterService
        
        service = EnhancedAICoverLetterService()
        test_cv = "Jane Smith, Data Scientist with machine learning expertise."
        
        analysis = service.analyze_cv_comprehensive(test_cv)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('overall_score', analysis)
        self.assertIn('ats_score', analysis)
        self.assertIn('keyword_score', analysis)
        self.assertIn('strengths', analysis)
        self.assertIn('weaknesses', analysis)
        self.assertIn('recommendations', analysis)
    
    def test_cover_letter_generation_fallback(self):
        # Test cover letter generation with fallback data
        from .ai_services import EnhancedAICoverLetterService
        
        service = EnhancedAICoverLetterService()
        
        cv_insights = {
            'skills': ['Python', 'Django'],
            'experience': ['5 years software development'],
            'achievements': ['Led team of 5 developers'],
            'summary': 'Experienced developer'
        }
        
        job_match = {
            'match_score': 85,
            'matching_skills': ['Python', 'Django'],
            'missing_skills': ['React'],
            'recommendations': ['Highlight leadership']
        }
        
        cover_letter = service.generate_tailored_cover_letter(
            cv_insights, job_match, "Software Engineer", "We need a Python developer."
        )
        
        self.assertIsInstance(cover_letter, str)
        self.assertGreater(len(cover_letter), 100)  # Should be a substantial letter
        self.assertIn('Software Engineer', cover_letter)

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_cv_model_creation(self):
        # Test CV model creation
        cv = CV.objects.create(
            title="Test CV",
            user=self.user
        )
        
        self.assertEqual(cv.title, "Test CV")
        self.assertEqual(cv.user, self.user)
        self.assertIsNotNone(cv.created_at)
    
    def test_cv_model_str(self):
        # Test CV model string representation
        cv = CV.objects.create(
            title="Test CV",
            user=self.user
        )
        
        expected_str = f"{cv.title} - {cv.user.username}"
        self.assertEqual(str(cv), expected_str)
