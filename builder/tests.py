from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CV, CoverLetter
from unittest.mock import patch

class BuilderViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Create a dummy CV instance. Adjust fields as necessary based on your CV model.
        self.cv = CV.objects.create(title="Test CV", user=self.user)
    
    def test_dashboard_view(self):
        # Verify that the dashboard view displays the created CV.
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cv.title)
    
    def test_create_cv_view_get(self):
        response = self.client.get(reverse('create_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/create_cv.html')
    
    def test_create_cv_view_post(self):
        # Test POST request for creating a new CV.
        data = {'title': 'New CV'}  # Adjust according to the actual fields required by CVForm.
        response = self.client.post(reverse('create_cv'), data)
        # Expect redirection upon successful creation.
        self.assertEqual(response.status_code, 302)
    
    def test_generate_cover_letter_view_get(self):
        response = self.client.get(reverse('generate_cover_letter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/generate_cover_letter.html')
    
    def test_generate_cover_letter_view_post_success(self):
        # Test POST request for generating a cover letter with mocking OpenAI's response.
        with patch('builder.views.openai.Completion.create') as mock_create:
            # Setup the mock response.
            mock_response = type('obj', (object,), {'choices': [type('obj', (object,), {'text': 'Test Cover Letter'})]})
            mock_create.return_value = mock_response
            
            data = {
                'cv': self.cv.id,
                'job_title': 'Developer',
                'job_description': 'Job description for testing.'
            }
            response = self.client.post(reverse('generate_cover_letter'), data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Cover Letter', response.content.decode())
