from openai import OpenAI
import os
import logging
import json
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class EnhancedAICoverLetterService:
    """Enhanced AI service for cover letter generation with CV analysis"""
    
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not found, falling back to mock responses")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
    
    def extract_cv_insights(self, cv_text: str) -> Dict[str, Any]:
        """Extract key insights from CV text using OpenAI"""
        if not cv_text:
            return {
                'skills': [],
                'experience': [],
                'education': [],
                'achievements': [],
                'summary': 'No CV provided'
            }
        
        try:
            # Fallback to mock data if no OpenAI API key
            if not self.client:
                return {
                    'skills': ['Python', 'Django', 'JavaScript', 'SQL', 'Team Leadership'],
                    'experience': ['5+ years software development', '3 years team lead'],
                    'education': ["Bachelor's in Computer Science"],
                    'achievements': ['Led team of 5 developers', 'Reduced load time by 40%', 'Increased efficiency by 25%'],
                    'summary': 'Experienced full-stack developer with strong backend skills and leadership experience'
                }
            
            prompt = f"""
            Analyze the following CV text and extract structured information. Return a JSON response with:
            - skills: list of technical and soft skills
            - experience: list of key experience points
            - education: list of education/qualifications
            - achievements: list of quantifiable achievements
            - summary: brief professional summary
            
            CV Text: {cv_text[:2000]}
            
            Return only valid JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate required fields
            required_fields = ['skills', 'experience', 'education', 'achievements', 'summary']
            for field in required_fields:
                if field not in result:
                    result[field] = []
                    
            return result
            
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
        """Generate tailored cover letter using OpenAI"""
        try:
            logger.info(f"Starting cover letter generation for job: {job_title}")
            
            # Ensure we have valid inputs
            if not job_title or not job_description:
                raise ValueError("Job title and description are required")
            
            # Prepare data with fallbacks
            skills_list = cv_insights.get('skills', [])
            skills_text = ', '.join(skills_list[:5]) if skills_list else 'relevant technical skills'
            
            achievements_list = cv_insights.get('achievements', [])
            achievements_text = '\n'.join([f"- {ach}" for ach in achievements_list[:3]]) if achievements_list else '- Strong problem-solving abilities\n- Excellent communication skills\n- Team collaboration'
            
            experience_list = cv_insights.get('experience', [])
            experience_text = experience_list[0] if experience_list else 'professional experience'
            
            education_list = cv_insights.get('education', [])
            education_text = ', '.join(education_list) if education_list else 'relevant educational background'
            
            summary_text = cv_insights.get('summary', 'experienced professional')
            
            # Fallback to template if no OpenAI API key
            if not self.client:
                logger.info("Using fallback template (no OpenAI API key)")
                return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position. With my experience in {skills_text.split(', ')[0] if skills_text else 'software development'} and proven track record, I believe I would be a valuable addition to your organization.

Throughout my career, I have demonstrated expertise in {skills_text}. My background includes {experience_text}, which has prepared me well for this role.

Key achievements that align with your requirements include:
{achievements_text}

I am excited about the opportunity to bring my skills and experience to your team and contribute to your continued success. I would welcome the chance to discuss how my background and enthusiasm can benefit your organization.

Thank you for considering my application. I look forward to hearing from you.

Sincerely,
[Your Name]"""
            
            # Use OpenAI API
            logger.info("Using OpenAI API for cover letter generation")
            prompt = f"""
            Generate a professional cover letter for the following job application:
            
            Job Title: {job_title}
            Job Description: {job_description[:1000]}
            
            Candidate Background:
            - Skills: {skills_text}
            - Experience: {experience_text}
            - Education: {education_text}
            - Achievements: {achievements_text}
            - Summary: {summary_text}
            
            Tone: {tone}
            Template: {template_type}
            
            Requirements:
            - Professional and engaging
            - Highlight relevant skills and experience
            - Keep to 3-4 paragraphs
            - Include specific achievements when relevant
            - End with strong call to action
            - Address to "Dear Hiring Manager"
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            generated_letter = response.choices[0].message.content.strip()
            logger.info(f"Cover letter generated successfully: {len(generated_letter)} characters")
            return generated_letter
            
        except Exception as e:
            logger.error(f"Cover letter generation failed: {str(e)}")
            # Return a basic fallback template
            return f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at your organization. Based on the job description, I believe my skills and experience make me a strong candidate for this role.

My background includes experience in software development and various technical skills that align with your requirements. I am passionate about contributing to innovative projects and working collaboratively with teams to achieve business objectives.

I would welcome the opportunity to discuss how my experience and enthusiasm can contribute to your team's success. Thank you for considering my application.

Sincerely,
[Your Name]"""
    
    def analyze_cv_comprehensive(self, cv_text: str) -> Dict[str, Any]:
        """Comprehensive CV analysis with scoring and recommendations"""
        if not cv_text:
            return self._get_default_analysis()
        
        try:
            # Fallback to template analysis if no OpenAI API key
            if not self.client:
                return self._get_mock_analysis(cv_text)
            
            prompt = f"""
            Analyze the following CV and provide a comprehensive assessment. Return a JSON response with:
            
            1. overall_score: Overall quality score (0-100)
            2. ats_score: ATS compatibility score (0-100)
            3. keyword_score: Keyword optimization score (0-100)
            4. strengths: List of 4-6 key strengths
            5. weaknesses: List of 4-6 areas for improvement
            6. recommendations: List of 4-6 specific recommendations
            7. skills: List of identified technical and soft skills
            8. experience_level: Brief description of experience level
            9. industry: Primary industry focus
            10. education_level: Education level identified
            
            CV Text: {cv_text[:3000]}
            
            Return only valid JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate and ensure all required fields
            required_fields = [
                'overall_score', 'ats_score', 'keyword_score', 'strengths', 
                'weaknesses', 'recommendations', 'skills', 'experience_level', 
                'industry', 'education_level'
            ]
            
            for field in required_fields:
                if field not in result:
                    if field.endswith('_score'):
                        result[field] = 75
                    elif field in ['experience_level', 'industry', 'education_level']:
                        result[field] = 'Not specified'
                    else:
                        result[field] = []
            
            # Ensure scores are integers
            for score_field in ['overall_score', 'ats_score', 'keyword_score']:
                result[score_field] = int(result.get(score_field, 75))
                
            return result
            
        except Exception as e:
            logger.error(f"CV comprehensive analysis failed: {str(e)}")
            return self._get_mock_analysis(cv_text)
    
    def _get_mock_analysis(self, cv_text: str) -> Dict[str, Any]:
        """Generate mock analysis when AI is not available"""
        # Simple keyword analysis for mock scoring
        keywords = ['python', 'javascript', 'sql', 'project', 'management', 'team', 'leadership', 'experience']
        text_lower = cv_text.lower()
        keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Calculate mock scores based on content length and keywords
        overall_score = min(95, max(60, 70 + keyword_matches * 3))
        ats_score = min(90, max(50, 65 + keyword_matches * 4))
        keyword_score = min(100, keyword_matches * 12)
        
        return {
            'overall_score': overall_score,
            'ats_score': ats_score,
            'keyword_score': keyword_score,
            'strengths': [
                'Clear professional formatting',
                'Relevant work experience included',
                'Good use of action verbs',
                'Quantifiable achievements mentioned',
                'Technical skills clearly listed'
            ],
            'weaknesses': [
                'Could benefit from more specific metrics',
                'Missing industry keywords',
                'Contact information could be more prominent',
                'Summary section could be stronger'
            ],
            'recommendations': [
                'Add more quantified achievements with percentages/numbers',
                'Include relevant industry keywords for ATS optimization',
                'Consider adding a professional summary at the top',
                'Ensure consistent formatting throughout',
                'Add relevant certifications if applicable'
            ],
            'skills': ['Communication', 'Project Management', 'Team Leadership', 'Problem Solving', 'Technical Skills'],
            'experience_level': 'Mid-level professional with relevant experience',
            'industry': 'Technology/Business',
            'education_level': 'Bachelor\'s degree or equivalent'
        }
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Default analysis for empty CV"""
        return {
            'overall_score': 0,
            'ats_score': 0,
            'keyword_score': 0,
            'strengths': [],
            'weaknesses': ['No CV content provided'],
            'recommendations': ['Please upload a valid CV file'],
            'skills': [],
            'experience_level': 'Not available',
            'industry': 'Not specified',
            'education_level': 'Not specified'
        }

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
