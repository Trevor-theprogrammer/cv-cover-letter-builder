from django.test import TestCase
from unittest.mock import patch, MagicMock
from builder.cv_analyzer import CVAnalyzer


class CVAnalyzerTest(TestCase):
    def setUp(self):
        self.analyzer = CVAnalyzer()
        self.sample_cv_text = """
        John Doe
        Software Developer
        Email: john.doe@email.com
        Phone: +1-555-123-4567
        
        Professional Summary:
        Experienced software developer with 5+ years in Python, Django, and React.
        
        Experience:
        Senior Developer at TechCorp (2020-2024)
        - Led development of web applications using Python and Django
        - Implemented RESTful APIs and microservices architecture
        
        Skills:
        - Python, Django, Flask
        - JavaScript, React, Vue.js
        - PostgreSQL, MongoDB
        - Docker, Kubernetes
        
        Education:
        Bachelor of Science in Computer Science, 2018
        """

    def test_extract_skills(self):
        skills = self.analyzer.extract_skills(self.sample_cv_text)
        expected_skills = ['Python', 'Django', 'React', 'JavaScript', 'PostgreSQL', 'MongoDB', 'Docker', 'Kubernetes']
        
        for skill in expected_skills:
            self.assertIn(skill, skills)

    def test_calculate_experience_years(self):
        experience = self.analyzer.calculate_experience_years(self.sample_cv_text)
        self.assertEqual(experience, 5)

    def test_extract_contact_info(self):
        contact_info = self.analyzer.extract_contact_info(self.sample_cv_text)
        
        self.assertEqual(contact_info['name'], 'John Doe')
        self.assertEqual(contact_info['email'], 'john.doe@email.com')
        self.assertEqual(contact_info['phone'], '+1-555-123-4567')
        self.assertEqual(contact_info['title'], 'Software Developer')

    def test_analyze_cv_complete(self):
        analysis = self.analyzer.analyze_cv(self.sample_cv_text)
        
        self.assertEqual(analysis['name'], 'John Doe')
        self.assertEqual(analysis['email'], 'john.doe@email.com')
        self.assertEqual(analysis['phone'], '+1-555-123-4567')
        self.assertEqual(analysis['title'], 'Software Developer')
        self.assertEqual(analysis['experience_years'], 5)
        self.assertIn('Python', analysis['skills'])
        self.assertIn('Django', analysis['skills'])

    def test_analyze_empty_cv(self):
        analysis = self.analyzer.analyze_cv("")
        
        self.assertEqual(analysis['name'], '')
        self.assertEqual(analysis['email'], '')
        self.assertEqual(analysis['phone'], '')
        self.assertEqual(analysis['title'], '')
        self.assertEqual(analysis['experience_years'], 0)
        self.assertEqual(analysis['skills'], [])

    def test_extract_skills_case_insensitive(self):
        cv_text = "python PYTHON django DJANGO"
        skills = self.analyzer.extract_skills(cv_text)
        
        # Should deduplicate skills
        self.assertEqual(len(skills), 2)
        self.assertIn('Python', skills)
        self.assertIn('Django', skills)

    def test_calculate_experience_from_various_formats(self):
        # Test different experience formats
        formats = [
            "5 years of experience",
            "5+ years experience",
            "5 years experience",
            "Experience: 5 years",
            "5 yrs experience"
        ]
        
        for text in formats:
            experience = self.analyzer.calculate_experience_years(text)
            self.assertEqual(experience, 5)

    def test_extract_skills_from_technical_keywords(self):
        technical_text = """
        Technologies: Python, Django, Flask, FastAPI, PostgreSQL, Redis, Docker, AWS
        Frameworks: React, Vue.js, Angular
        Tools: Git, Jenkins, Docker, Kubernetes
        """
        
        skills = self.analyzer.extract_skills(technical_text)
        expected = ['Python', 'Django', 'Flask', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'AWS', 'React', 'Vue.js', 'Angular', 'Git', 'Jenkins']
        
        for skill in expected:
            self.assertIn(skill, skills)
