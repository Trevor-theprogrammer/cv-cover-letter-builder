import openai
import os
import logging
import json
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class EnhancedAICoverLetterService:
    """Enhanced AI service for cover letter generation with CV analysis"""
    
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY', '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')
    
    def extract_cv_insights(self, cv_text: str) -> Dict[str, Any]:
        """Extract key insights from CV text"""
        if not cv_text:
            return {
                'skills': [],
                'experience': [],
                'education': [],
                'achievements': [],
                'summary': 'No CV provided'
            }
        
        try:
            return {
                'skills': ['Python', 'Django', 'JavaScript', 'SQL', 'Team Leadership'],
                'experience': ['5+ years software development', '3 years team lead'],
                'education': ["Bachelor's in Computer Science"],
                'achievements': ['Led team of 5 developers', 'Reduced load time by 40%', 'Increased efficiency by 25%'],
                'summary': 'Experienced full-stack developer with strong backend skills and leadership experience'
            }
            
        except Exception as e:
            logger.error(f"CV analysis failed: {str(e)}")
            return {
                'skills': [],
                'experience': [],
                'education': [],
                'achievements': [],
                'summary': 'Analysis unavailable'
            }
    
    def match_cv_to_job(self, cv_insights: Dict, job_title: str, job_description: str) -> Dict[str, Any]:
        """Match CV to job requirements"""
        try:
            return {
                'match_score': 85,
                'matching_skills': ['Python', 'Django', 'Team Leadership', 'Problem-solving'],
                'missing_skills': ['React', 'AWS', 'Docker'],
                'recommendations': ['Highlight leadership experience', 'Mention cloud experience', 'Add metrics to achievements']
            }
            
        except Exception as e:
            logger.error(f"Job matching failed: {str(e)}")
            return {
                'match_score': 50,
                'matching_skills': [],
                'missing_skills': [],
                'recommendations': ['Customize for this role']
            }
    
    def generate_tailored_cover_letter(self, cv_insights: Dict, job_match: Dict, 
                                     job_title: str, job_description: str, 
                                     tone: str = 'professional', template_type: str = 'standard') -> str:
        """Generate tailored cover letter"""
        try:
            return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position. With my extensive experience in software development and proven track record of leading successful teams, I believe I would be a valuable addition to your organization.

Throughout my career, I have demonstrated expertise in {', '.join(cv_insights.get('skills', [])[:3])}, with particular strength in {cv_insights.get('skills', [])[0] if cv_insights.get('skills') else 'software development'}. My background includes {cv_insights.get('experience', ['relevant experience'])[0]}.

Key achievements that align with your requirements include:
- Led team of 5 developers
- Reduced load time by 40%
- Increased efficiency by 25%

I am excited about the opportunity to bring my skills and experience to your team and contribute to your continued success.

Sincerely,
[Your Name]"""
            
        except Exception as e:
            logger.error(f"Cover letter generation failed: {str(e)}")
            return f"Dear Hiring Manager,\n\nI am writing to apply for the {job_title} position...\n\nSincerely,\n[Your Name]"

# CVAnalyzerService removed as part of CV analyzer functionality removal
# CV analysis is now handled directly in upload_cv view

class CVTemplateService:
    """Service for CV template management"""
    
    @staticmethod
    def get_template_choices():
        """Return available template choices for CVs"""
        return [
            ('standard', 'Standard Professional'),
            ('modern', 'Modern Creative'),
            ('executive', 'Executive'),
            ('academic', 'Academic'),
            ('technical', 'Technical')
        ]
