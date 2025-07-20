from django.test import TestCase
from unittest.mock import patch, MagicMock
from builder.ai_services import AICoverLetterGenerator


class AICoverLetterGeneratorTest(TestCase):
    def setUp(self):
        self.generator = AICoverLetterGenerator()
        self.cv_text = "Software developer with 5 years experience in Python and Django"
        self.job_description = "Looking for a Python developer with Django experience"

    @patch('builder.ai_services.openai.ChatCompletion.create')
    def test_generate_cover_letter_success(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Dear Hiring Manager..."
        mock_openai.return_value = mock_response

        result = self.generator.generate_cover_letter(
            cv_text=self.cv_text,
            job_description=self.job_description
        )
        
        self.assertEqual(result, "Dear Hiring Manager...")
        mock_openai.assert_called_once()

    @patch('builder.ai_services.openai.ChatCompletion.create')
    def test_generate_cover_letter_empty_response(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        mock_openai.return_value = mock_response

        result = self.generator.generate_cover_letter(
            cv_text=self.cv_text,
            job_description=self.job_description
        )
        
        self.assertEqual(result, "Unable to generate cover letter at this time.")

    def test_validate_inputs(self):
        with self.assertRaises(ValueError):
            self.generator.generate_cover_letter("", self.job_description)
        
        with self.assertRaises(ValueError):
            self.generator.generate_cover_letter(self.cv_text, "")


# CVAnalyzer tests removed as part of CV analyzer functionality removal
