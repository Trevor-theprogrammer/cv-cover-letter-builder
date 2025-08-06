from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock
import tempfile
import os
from builder.models import UploadedCV, CVAnalysis, AICoverLetter


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')


class HomeViewTest(BaseTestCase):
    def test_home_view_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/home.html')


class DashboardViewTest(BaseTestCase):
    def test_dashboard_view_authenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/dashboard.html')

    def test_dashboard_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class UploadCVViewTest(BaseTestCase):
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_upload_cv_get(self):
        response = self.client.get(reverse('upload_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/upload_cv.html')

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_upload_cv_post_valid(self):
        pdf_content = b'%PDF-1.4\n%Test PDF content'
        file = SimpleUploadedFile(
            "test.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        response = self.client.post(reverse('upload_cv'), {
            'cv_file': file,
            'title': 'Test CV'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(UploadedCV.objects.filter(user=self.user).exists())

    def test_upload_cv_post_invalid(self):
        response = self.client.post(reverse('upload_cv'), {})
        self.assertEqual(response.status_code, 200)  # Form errors
        self.assertFormError(response, 'form', 'cv_file', 'This field is required.')


class GenerateCoverLetterViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file='test_cv.pdf',
            original_filename='test_cv.pdf'
        )

    def test_generate_cover_letter_get(self):
        response = self.client.get(reverse('generate_cover_letter', args=[self.uploaded_cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/generate_cover_letter.html')

    def test_generate_cover_letter_post(self):
        with patch('builder.views.AICoverLetterGenerator.generate_cover_letter') as mock_generate:
            mock_generate.return_value = "Generated cover letter content"
            
            response = self.client.post(reverse('generate_cover_letter', args=[self.uploaded_cv.id]), {
                'job_description': 'Software Developer position',
                'company_name': 'TechCorp',
                'tone': 'professional'
            })
            
            self.assertEqual(response.status_code, 302)
            self.assertTrue(AICoverLetter.objects.filter(user=self.user).exists())

    def test_generate_cover_letter_invalid_cv(self):
        response = self.client.get(reverse('generate_cover_letter', args=[999]))
        self.assertEqual(response.status_code, 404)


class CVDetailViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file='test_cv.pdf',
            original_filename='test_cv.pdf'
        )
        self.analysis = CVAnalysis.objects.create(
            uploaded_cv=self.uploaded_cv,
            extracted_text='Test CV content',
            skills=['Python', 'Django'],
            experience_years=5
        )

    def test_cv_detail_view(self):
        response = self.client.get(reverse('cv_detail', args=[self.uploaded_cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/cv_detail.html')
        self.assertContains(response, 'Test CV content')

    def test_cv_detail_view_other_user(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        
        response = self.client.get(reverse('cv_detail', args=[self.uploaded_cv.id]))
        self.assertEqual(response.status_code, 404)  # Should not see other user's CV


class APIEndpointsTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file='test_cv.pdf',
            original_filename='test_cv.pdf'
        )

    def test_api_cv_list(self):
        response = self.client.get('/api/cvs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_cv.pdf')

    def test_api_cv_detail(self):
        response = self.client.get(f'/api/cvs/{self.uploaded_cv.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_cv.pdf')

    def test_api_cover_letters_list(self):
        AICoverLetter.objects.create(
            user=self.user,
            uploaded_cv=self.uploaded_cv,
            job_description='Test job',
            generated_text='Test cover letter'
        )
        
        response = self.client.get('/api/cover-letters/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test job')


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_login_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_post_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
