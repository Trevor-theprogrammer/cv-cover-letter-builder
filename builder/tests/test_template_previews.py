from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

class TemplatePreviewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_previews_gallery(self):
        """Test the template previews gallery view"""
        response = self.client.get(reverse('builder:template_previews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder/template_previews.html')

    def test_valid_template_preview(self):
        """Test valid individual template preview"""
        template_names = ['modern', 'classic', 'minimal', 'creative']
        for template_name in template_names:
            response = self.client.get(
                reverse('builder:template_preview', 
                       kwargs={'template_name': template_name}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, f'builder/templates/{template_name}_preview.html')

    def test_invalid_template_preview(self):
        """Test invalid template preview request"""
        response = self.client.get(
            reverse('builder:template_preview', 
                   kwargs={'template_name': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
        
        # Check for warning message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Template \'nonexistent\' not found', 
                     str(messages[0]))
