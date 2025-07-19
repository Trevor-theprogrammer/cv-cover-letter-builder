from django.test import TestCase
from django.contrib.auth.models import User
from builder.models import (
    Template, UploadedCV, CVAnalysis, AICoverLetter
)


class TemplateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.template = Template.objects.create(
            name='Test Template',
            description='A test template',
            created_by=self.user
        )

    def test_template_creation(self):
        self.assertEqual(self.template.name, 'Test Template')
        self.assertEqual(self.template.created_by, self.user)


class UploadedCVModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file='test_cv.pdf',
            original_filename='test_cv.pdf'
        )

    def test_uploaded_cv_creation(self):
        self.assertEqual(self.uploaded_cv.user, self.user)
        self.assertEqual(self.uploaded_cv.original_filename, 'test_cv.pdf')


class CVAnalysisModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file='test_cv.pdf',
            original_filename='test_cv.pdf'
        )
        self.analysis = CVAnalysis.objects.create(
            uploaded_cv=self.uploaded_cv,
            extracted_text='Test extracted text',
            skills=['Python', 'Django'],
            experience_years=5
        )

    def test_cv_analysis_creation(self):
        self.assertEqual(self.analysis.uploaded_cv, self.uploaded_cv)
        self.assertEqual(self.analysis.skills, ['Python', 'Django'])


class AICoverLetterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file='test_cv.pdf',
            original_filename='test_cv.pdf'
        )
        self.cover_letter = AICoverLetter.objects.create(
            user=self.user,
            uploaded_cv=self.uploaded_cv,
            job_description='Software Developer position',
            generated_text='Dear Hiring Manager...'
        )

    def test_ai_cover_letter_creation(self):
        self.assertEqual(self.cover_letter.user, self.user)
        self.assertEqual(self.cover_letter.job_description, 'Software Developer position')
