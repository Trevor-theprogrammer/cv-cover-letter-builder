import openai
from django.conf import settings
import json
import re
from typing import Dict, List, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EnhancedAICoverLetterService:
    """Enhanced service for generating highly personalized AI cover letters"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY if hasattr(settings, 'OPENAI_API_KEY') else None
        if not self.api_key:
            self.api_key = "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"
    
    def extract_cv_insights(self, cv_text: str) -> Dict[str, Any]:
        """Deeply analyze CV to extract key insights, achievements, and metrics"""
        
        if not self.api_key:
            return self._get_mock_cv_insights()
        
        prompt = f"""
        You are an expert career coach and resume analyst. Perform a deep analysis of this CV to extract actionable insights for cover letter generation.

        CV CONTENT:
        {cv_text}

        Extract the following information in JSON format:
        {{
            "key_achievements": [
                {{
                    "achievement": "specific accomplishment",
                    "metric": "quantifiable result (number, percentage, etc.)",
                    "context": "where/when this happened",
                    "relevance_score": 1-10
                }}
            ],
            "core_skills": [
                {{
                    "skill": "technical or soft skill",
                    "proficiency_level": "beginner|intermediate|advanced|expert",
                    "years_experience": number,
                    "evidence": "specific example from CV"
                }}
            ],
            "career_progression": [
                {{
                    "role": "job title",
                    "company": "company name",
                    "duration": "time period",
                    "key_responsibilities": ["main responsibility 1", "main responsibility 2"],
                    "promotion": true/false
                }}
            ],
            "industry_expertise": ["specific industries worked in"],
            "leadership_experience": [
                {{
                    "role": "leadership position",
                    "team_size": number,
                    "achievement": "specific leadership accomplishment"
                }}
            ],
            "problem_solving_examples": [
                {{
                    "problem": "challenge faced",
                    "solution": "approach taken",
                    "result": "measurable outcome"
                }}
            ],
            "unique_value_props": ["3-5 unique selling points based on CV"],
            "career_narrative": "2-3 sentence career story that connects past to future"
        }}

        Focus on specific, quantifiable achievements and concrete examples. Be extremely detailed and extract maximum value from the CV content.
        """
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career coach who extracts maximum value from CVs for personalized cover letters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            insights_text = response.choices[0].message.content.strip()
            insights_text = re.sub(r'```json\s*|\s*```', '', insights_text)
            return json.loads(insights_text)
            
        except Exception as e:
            return self._get_mock_cv_insights()
    
    def match_cv_to_job(self, cv_insights: Dict[str, Any], job_title: str, job_description: str) -> Dict[str, Any]:
        """Match CV content to job requirements using semantic analysis"""
        
        if not self.api_key:
            return self._get_mock_job_match()
        
        prompt = f"""
        You are an expert recruiter analyzing how well a candidate's CV matches a job posting.

        CANDIDATE PROFILE:
        {json.dumps(cv_insights, indent=2)}

        JOB TARGET:
        Title: {job_title}
        Description: {job_description}

        Provide a detailed matching analysis in JSON format:
        {{
            "overall_match_score": 0-100,
            "top_matching_skills": [
                {{
                    "skill": "skill name",
                    "cv_evidence": "specific example from CV",
                    "job_requirement": "how it matches job",
                    "relevance_score": 1-10
                }}
            ],
            "skill_gaps": [
                {{
                    "missing_skill": "required skill not in CV",
                    "alternative": "related skill or experience that compensates",
                    "compensation_strategy": "how to address this gap"
                }}
            ],
            "experience_alignment": {{
                "years_required": "years specified in job",
                "years_candidate_has": "relevant years from CV",
                "alignment_score": 1-10,
                "explanation": "why experience is sufficient"
            }},
            "key_achievements_to_highlight": [
                {{
                    "achievement": "specific accomplishment",
                    "job_relevance": "why this matters for the role",
                    "presentation": "how to phrase this in cover letter"
                }}
            ],
            "company_fit_indicators": [
                "specific reasons candidate would excel at this company"
            ],
            "unique_angles": [
                "unexpected ways candidate's background adds value"
            ],
            "addressing_gaps": [
                "how to frame any potential concerns positively"
            ]
        }}

        Be specific and provide actionable insights for the cover letter.
        """
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert recruiter who provides detailed job matching analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            match_text = response.choices[0].message.content.strip()
            match_text = re.sub(r'```json\s*|\s*```', '', match_text)
            return json.loads(match_text)
            
        except Exception as e:
            return self._get_mock_job_match()
    
    def generate_tailored_cover_letter(self, cv_insights: Dict[str, Any], job_match: Dict[str, Any], 
                                     job_title: str, job_description: str, tone: str = 'professional',
                                     template_type: str = 'standard') -> str:
        """Generate highly personalized cover letter using CV insights and job matching"""
        
        if not self.api_key:
            return self._get_mock_cover_letter(job_title, cv_insights)
        
        # Build context from insights and matching
        achievements_context = "\n".join([
            f"- {ach['achievement']} ({ach['metric']}) in {ach['context']}"
            for ach in cv_insights.get('key_achievements', [])[:3]
        ])
        
        skills_context = "\n".join([
            f"- {skill['skill']} ({skill['proficiency_level']}, {skill['years_experience']} years): {skill['evidence']}"
            for skill in cv_insights.get('core_skills', [])[:5]
        ])
        
        matching_context = "\n".join([
            f"- {match['skill']}: {match['presentation']}"
            for match in job_match.get('key_achievements_to_highlight', [])
        ])
        
        prompt = f"""
        You are a world-class career strategist writing a cover letter that will guarantee an interview. Use the provided insights to create a masterpiece.

        CANDIDATE INSIGHTS:
        {json.dumps(cv_insights, indent=2)}

        JOB MATCHING ANALYSIS:
        {json.dumps(job_match, indent=2)}

        JOB DETAILS:
        Title: {job_title}
        Description: {job_description}

        WRITING STYLE: {tone}
        TEMPLATE TYPE: {template_type}

        REQUIREMENTS:
        1. Start with a compelling hook that shows deep company knowledge
        2. Tell the candidate's unique career story using specific achievements
        3. Address each key job requirement with concrete CV evidence
        4. Include 3-4 quantifiable achievements with metrics
        5. Show company fit with specific research
        6. Address any skill gaps positively
        7. End with a clear call to action
        8. Use natural, engaging language (not corporate speak)
        9. Keep to 300-400 words
        10. Make it impossible to ignore this candidate

        Write a cover letter that will make the hiring manager immediately schedule an interview:
        """
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are the world's best cover letter writer who creates irresistible, personalized letters that get interviews."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._get_mock_cover_letter(job_title, cv_insights)
    
    def _get_mock_cv_insights(self) -> Dict[str, Any]:
        """Mock CV insights for testing without API"""
        return {
            "key_achievements": [
                {
                    "achievement": "Increased sales revenue",
                    "metric": "35% growth",
                    "context": "Q3 2023 at TechCorp",
                    "relevance_score": 9
                },
                {
                    "achievement": "Reduced operational costs",
                    "metric": "$50K savings annually",
                    "context": "Process optimization project",
                    "relevance_score": 8
                },
                {
                    "achievement": "Led digital transformation",
                    "metric": "200% efficiency improvement",
                    "context": "Cross-department initiative",
                    "relevance_score": 10
                }
            ],
            "core_skills": [
                {
                    "skill": "Project Management",
                    "proficiency_level": "expert",
                    "years_experience": 7,
                    "evidence": "PMP certified, led 50+ projects"
                },
                {
                    "skill": "Data Analysis",
                    "proficiency_level": "advanced",
                    "years_experience": 5,
                    "evidence": "SQL, Python, Tableau expertise"
                },
                {
                    "skill": "Team Leadership",
                    "proficiency_level": "advanced",
                    "years_experience": 4,
                    "evidence": "Managed teams of 5-15 people"
                }
            ],
            "career_progression": [
                {
                    "role": "Senior Project Manager",
                    "company": "TechCorp",
                    "duration": "2021-Present",
                    "key_responsibilities": ["Strategic planning", "Team leadership", "Budget management"],
                    "promotion": True
                },
                {
                    "role": "Project Manager",
                    "company": "StartUp Inc",
                    "duration": "2019-2021",
                    "key_responsibilities": ["Project delivery", "Client management", "Process improvement"],
                    "promotion": False
                }
            ],
            "industry_expertise": ["Technology", "Finance", "Healthcare"],
            "leadership_experience": [
                {
                    "role": "Project Lead",
                    "team_size": 12,
                    "achievement": "Delivered 95% of projects on time and under budget"
                }
            ],
            "problem_solving_examples": [
                {
                    "problem": "Legacy system inefficiency",
                    "solution": "Implemented cloud-based solution",
                    "result": "60% cost reduction and 3x speed improvement"
                }
            ],
            "unique_value_props": [
                "Proven track record of delivering complex projects",
                "Strong technical background with business acumen",
                "Exceptional team leadership and mentoring skills",
                "Data-driven decision making expertise"
            ],
            "career_narrative": "Results-driven professional with 7+ years of progressive experience in project management, combining technical expertise with strategic business acumen to deliver measurable impact across technology, finance, and healthcare sectors."
        }
    
    def _get_mock_job_match(self) -> Dict[str, Any]:
        """Mock job matching for testing without API"""
        return {
            "overall_match_score": 92,
            "top_matching_skills": [
                {
                    "skill": "Project Management",
                    "cv_evidence": "7 years experience, PMP certified, led 50+ projects",
                    "job_requirement": "Manage complex technical projects",
                    "relevance_score": 10
                },
                {
                    "skill": "Team Leadership",
                    "cv_evidence": "Managed teams of 5-15 people, 95% project success rate",
                    "job_requirement": "Lead cross-functional teams",
                    "relevance_score": 9
                }
            ],
            "skill_gaps": [],
            "experience_alignment": {
                "years_required": "5-7",
                "years_candidate_has": "7",
                "alignment_score": 10,
                "explanation": "Exceeds minimum requirements with proven track record"
            },
            "key_achievements_to_highlight": [
                {
                    "achievement": "35% sales revenue increase",
                    "job_relevance": "Demonstrates ability to drive business results",
                    "presentation": "Drove 35% revenue growth through strategic project initiatives"
                },
                {
                    "achievement": "200% efficiency improvement",
                    "job_relevance": "Shows process optimization expertise",
                    "presentation": "Led digital transformation achieving 200% efficiency gains"
                }
            ],
            "company_fit_indicators": [
                "Strong alignment with innovation-focused culture",
                "Proven experience in target industries",
                "Track record of measurable business impact"
            ],
            "unique_angles": [
                "Cross-industry perspective brings fresh insights",
                "Technical background enables better stakeholder communication"
            ],
            "addressing_gaps": []
        }
    
    def _get_mock_cover_letter(self, job_title: str, cv_insights: Dict[str, Any]) -> str:
        """Mock cover letter for testing without API"""
        return f"""Dear Hiring Manager,

Your search for an exceptional {job_title} ends today. With seven years of proven project management expertise and a track record of delivering 35% revenue growth, I'm excited to bring my strategic leadership to your team.

Throughout my career, I've consistently transformed complex challenges into measurable business results:

• Led 50+ successful projects with 95% on-time delivery, managing teams of up to 15 professionals
• Drove 35% revenue growth through strategic project initiatives and process optimization
• Achieved 200% efficiency improvement through digital transformation leadership
• Delivered $50K annual cost savings through innovative operational improvements

My unique combination of technical expertise and business acumen enables me to bridge the gap between complex technical requirements and strategic business objectives. Having successfully delivered projects across technology, finance, and healthcare sectors, I bring cross-industry insights that drive innovation.

I'm particularly drawn to your organization's commitment to innovation and believe my proven ability to deliver measurable results aligns perfectly with your goals. My data-driven approach and collaborative leadership style have consistently produced exceptional outcomes.

I would welcome the opportunity to discuss how my experience and passion for excellence can contribute to your continued success. Let's schedule a conversation to explore how I can help drive your next breakthrough initiative.

Best regards,
[Your Name]"""

class CVTemplateService:
    """Service for managing cover letter templates"""
    
    TEMPLATES = {
        'standard': {
            'name': 'Standard Professional',
            'structure': ['Hook', 'Experience', 'Skills', 'Company Fit', 'Call to Action']
        },
        'storytelling': {
            'name': 'Storytelling',
            'structure': ['Compelling Story', 'Challenge-Solution', 'Results', 'Future Vision']
        },
        'metrics_focused': {
            'name': 'Metrics-Focused',
            'structure': ['Hook with Metric', '3 Key Achievements', 'Skills Match', 'Close']
        },
        'creative': {
            'name': 'Creative & Bold',
            'structure': ['Attention Grabber', 'Unique Value', 'Proof Points', 'Memorable Close']
        }
    }
    
    @classmethod
    def get_template_choices(cls):
        """Get template choices for forms"""
        return [(key, value['name']) for key, value in cls.TEMPLATES.items()]
    
    @classmethod
    def apply_template_structure(cls, content: str, template_type: str) -> str:
        """Apply template structure to generated content"""
        # This would format the content according to template structure
        return content
