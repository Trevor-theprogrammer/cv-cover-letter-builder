from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
from unittest.mock import patch
import tempfile
import os
from builder.models import CV, UploadedCV, CoverLetter


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


class GenerateCoverLetterViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cv = CV.objects.create(
            user=self.user,
            title='Test CV',
            full_name='Test User'
        )

    def test_generate_cover_letter_get(self):
        response = self.client.get(reverse('generate_cover_letter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/generate_cover_letter.html')


class CVDetailViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cv = CV.objects.create(
            user=self.user,
            title='Test CV',
            full_name='Test User'
        )

    def test_cv_detail_view(self):
        response = self.client.get(reverse('cv_detail', args=[self.cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/cv_detail.html')
        self.assertContains(response, 'Test CV')


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

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
