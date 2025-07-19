from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import tempfile
import os
from builder.file_handlers import CVFileHandler
from builder.models import UploadedCV


class CVFileHandlerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.handler = CVFileHandler()
        
    def test_validate_pdf_file(self):
        pdf_content = b'%PDF-1.4\n%Test PDF content'
        file = SimpleUploadedFile(
            "test.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        self.assertTrue(self.handler.validate_file(file))

    def test_validate_docx_file(self):
        docx_content = b'PK\x03\x04\x14\x00\x06\x00'  # DOCX signature
        file = SimpleUploadedFile(
            "test.docx",
            docx_content,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        self.assertTrue(self.handler.validate_file(file))

    def test_validate_invalid_file(self):
        invalid_content = b'This is not a valid file'
        file = SimpleUploadedFile(
            "test.txt",
            invalid_content,
            content_type="text/plain"
        )
        self.assertFalse(self.handler.validate_file(file))

    def test_validate_large_file(self):
        large_content = b'x' * (6 * 1024 * 1024)  # 6MB file
        file = SimpleUploadedFile(
            "large.pdf",
            large_content,
            content_type="application/pdf"
        )
        self.assertFalse(self.handler.validate_file(file))

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_save_file(self):
        pdf_content = b'%PDF-1.4\n%Test PDF content'
        file = SimpleUploadedFile(
            "test.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        saved_path = self.handler.save_file(file, self.user)
        self.assertTrue(saved_path.endswith('.pdf'))
        self.assertTrue(os.path.exists(saved_path))

    def test_extract_text_from_pdf(self):
        # Mock PDF content for testing
        pdf_content = b'%PDF-1.4\n%Test PDF content\n(Hello World)'
        text = self.handler.extract_text_from_pdf(pdf_content)
        self.assertIsInstance(text, str)

    def test_extract_text_from_docx(self):
        # This would need a proper DOCX file for testing
        # For now, test the method exists and handles errors gracefully
        docx_content = b'PK\x03\x04\x14\x00\x06\x00'
        text = self.handler.extract_text_from_docx(docx_content)
        self.assertIsInstance(text, str)


class UploadedCVIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_upload_cv_flow(self):
        pdf_content = b'%PDF-1.4\n%Test PDF content'
        file = SimpleUploadedFile(
            "test.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        uploaded_cv = UploadedCV.objects.create(
            user=self.user,
            file=file,
            original_filename='test.pdf'
        )
        
        self.assertEqual(uploaded_cv.user, self.user)
        self.assertEqual(uploaded_cv.original_filename, 'test.pdf')
        self.assertTrue(uploaded_cv.file.name.endswith('.pdf'))
