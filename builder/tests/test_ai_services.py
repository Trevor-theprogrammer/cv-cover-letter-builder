from django.test import TestCase
from unittest.mock import patch, MagicMock
from builder.ai_services import AICoverLetterGenerator, CVAnalyzer


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


class CVAnalyzerTest(TestCase):
    def setUp(self):
        self.analyzer = CVAnalyzer()
        self.cv_text = """
        John Doe
        Software Developer
        Experience: 5 years Python, Django, React
        Skills: Python, Django, JavaScript, SQL
        Education: BS Computer Science
        """

    def test_extract_skills(self):
        skills = self.analyzer.extract_skills(self.cv_text)
        expected_skills = ['Python', 'Django', 'React', 'JavaScript', 'SQL']
        for skill in expected_skills:
            self.assertIn(skill, skills)

    def test_calculate_experience_years(self):
        experience = self.analyzer.calculate_experience_years(self.cv_text)
        self.assertEqual(experience, 5)

    def test_extract_contact_info(self):
        contact_info = self.analyzer.extract_contact_info(self.cv_text)
        self.assertEqual(contact_info['name'], 'John Doe')
        self.assertEqual(contact_info['title'], 'Software Developer')

    def test_analyze_empty_cv(self):
        analysis = self.analyzer.analyze_cv("")
        self.assertEqual(analysis['skills'], [])
        self.assertEqual(analysis['experience_years'], 0)
