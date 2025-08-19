"""
Enhanced CV Analysis Service for CV Cover Letter Builder
Provides comprehensive CV analysis, scoring, and improvement recommendations
"""

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass
class CVAnalysisResult:
    """Structure for CV analysis results"""
    overall_score: float
    ats_score: float
    keyword_matches: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
    section_scores: Dict[str, float]
    improvements: List[Dict[str, str]]
    industry_match: float
    experience_level: str

class CVAnalyzer:
    """Advanced CV analysis service"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Industry-specific keywords
        self.industry_keywords = {
            'software_engineering': [
                'python', 'javascript', 'java', 'react', 'angular', 'vue', 'node.js',
                'sql', 'mongodb', 'postgresql', 'aws', 'docker', 'kubernetes', 'git',
                'agile', 'scrum', 'microservices', 'rest api', 'ci/cd', 'tdd'
            ],
            'data_science': [
                'python', 'r', 'sql', 'machine learning', 'deep learning', 'statistics',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'tableau',
                'power bi', 'data visualization', 'regression', 'classification', 'nlp'
            ],
            'marketing': [
                'digital marketing', 'seo', 'sem', 'social media', 'content marketing',
                'google analytics', 'facebook ads', 'email marketing', 'branding',
                'campaign management', 'market research', 'crm', 'marketing automation'
            ],
            'finance': [
                'financial analysis', 'excel', 'sql', 'power bi', 'tableau', 'modeling',
                'forecasting', 'budgeting', 'reporting', 'accounting', 'investment',
                'risk management', 'compliance', 'auditing', 'financial statements'
            ]
        }
        
        # Experience level indicators
        self.experience_indicators = {
            'entry': ['intern', 'junior', 'entry level', 'graduate', 'trainee'],
            'mid': ['mid-level', 'senior', 'lead', 'specialist', 'analyst'],
            'senior': ['senior', 'principal', 'director', 'manager', 'head of', 'vp']
        }

    def analyze_cv(self, cv_text: str, job_description: str = None, industry: str = None) -> CVAnalysisResult:
        """Perform comprehensive CV analysis"""
        
        # Basic preprocessing
        cv_text = self._preprocess_text(cv_text)
        job_desc_text = self._preprocess_text(job_description) if job_description else ""
        
        # Calculate scores
        overall_score = self._calculate_overall_score(cv_text)
        ats_score = self._calculate_ats_score(cv_text, job_desc_text)
        
        # Extract keywords
        keyword_matches = self._extract_keywords(cv_text, industry)
        missing_keywords = self._find_missing_keywords(cv_text, job_desc_text, industry)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(cv_text, job_desc_text, industry)
        
        # Section analysis
        section_scores = self._analyze_sections(cv_text)
        
        # Experience level
        experience_level = self._determine_experience_level(cv_text)
        
        # Industry match
        industry_match = self._calculate_industry_match(cv_text, industry)
        
        # Improvements
        improvements = self._generate_improvements(cv_text, job_desc_text)
        
        return CVAnalysisResult(
            overall_score=overall_score,
            ats_score=ats_score,
            keyword_matches=keyword_matches,
            missing_keywords=missing_keywords,
            suggestions=suggestions,
            section_scores=section_scores,
            improvements=improvements,
            industry_match=industry_match,
            experience_level=experience_level
        )
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Convert to lowercase
        text = text.lower()
        return text.strip()
    
    def _calculate_overall_score(self, cv_text: str) -> float:
        """Calculate overall CV quality score"""
        score = 50  # Base score
        
        # Check for essential sections
        sections = ['experience', 'education', 'skills', 'summary', 'contact']
        for section in sections:
            if section in cv_text:
                score += 10
        
        # Check for quantifiable achievements
        numbers = re.findall(r'\d+', cv_text)
        if len(numbers) > 5:
            score += 10
        
        # Check for action verbs
        action_verbs = ['achieved', 'managed', 'developed', 'implemented', 'increased', 'reduced']
        verb_count = sum(1 for verb in action_verbs if verb in cv_text)
        score += min(verb_count * 2, 10)
        
        return min(score, 100)
    
    def _calculate_ats_score(self, cv_text: str, job_desc: str) -> float:
        """Calculate ATS compatibility score"""
        if not job_desc:
            return 75  # Default score without job description
        
        # Calculate keyword similarity
        cv_words = set(cv_text.split())
        job_words = set(job_desc.split())
        
        common_words = cv_words.intersection(job_words)
        similarity = len(common_words) / max(len(job_words), 1) * 100
        
        # Adjust for technical terms
        technical_terms = ['python', 'java', 'sql', 'javascript', 'react', 'angular']
        tech_matches = sum(1 for term in technical_terms if term in cv_text and term in job_desc)
        
        final_score = (similarity * 0.7) + (tech_matches * 3)
        return min(final_score, 100)
    
    def _extract_keywords(self, cv_text: str, industry: str = None) -> List[str]:
        """Extract relevant keywords from CV"""
        keywords = []
        
        # Extract technical skills
        doc = self.nlp(cv_text)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'TECHNOLOGY']:
                keywords.append(ent.text.lower())
        
        # Add industry-specific keywords
        if industry and industry in self.industry_keywords:
            industry_kw = self.industry_keywords[industry]
            keywords.extend([kw for kw in industry_kw if kw in cv_text])
        
        return list(set(keywords))
    
    def _find_missing_keywords(self, cv_text: str, job_desc: str, industry: str = None) -> List[str]:
        """Find keywords missing from CV compared to job description"""
        if not job_desc:
            return []
        
        cv_keywords = set(self._extract_keywords(cv_text, industry))
        job_keywords = set(self._extract_keywords(job_desc, industry))
        
        return list(job_keywords - cv_keywords)
    
    def _generate_suggestions(self, cv_text: str, job_desc: str, industry: str = None) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Length check
        if len(cv_text.split()) < 200:
            suggestions.append("Consider adding more detail to your experience sections")
        
        # Quantifiable achievements
        if not re.search(r'\d+', cv_text):
            suggestions.append("Add quantifiable achievements with numbers and percentages")
        
        # Action verbs
        action_verbs = ['achieved', 'managed', 'developed', 'led', 'implemented']
        if not any(verb in cv_text for verb in action_verbs):
            suggestions.append("Use more action verbs to describe your accomplishments")
        
        # Industry-specific suggestions
        if industry:
            industry_suggestions = self._get_industry_suggestions(industry)
            suggestions.extend(industry_suggestions)
        
        return suggestions
    
    def _analyze_sections(self, cv_text: str) -> Dict[str, float]:
        """Analyze individual CV sections"""
        sections = {
            'contact': 0,
            'summary': 0,
            'experience': 0,
            'education': 0,
            'skills': 0,
            'certifications': 0
        }
        
        # Check for section presence
        section_patterns = {
            'contact': r'(phone|email|address|linkedin)',
            'summary': r'(summary|objective|profile)',
            'experience': r'(experience|employment|work history)',
            'education': r'(education|degree|university|college)',
            'skills': r'(skills|technologies|competencies)',
            'certifications': r'(certifications|certificates|licenses)'
        }
        
        for section, pattern in section_patterns.items():
            if re.search(pattern, cv_text, re.IGNORECASE):
                sections[section] = 100
        
        return sections
    
    def _determine_experience_level(self, cv_text: str) -> str:
        """Determine candidate's experience level"""
        text_lower = cv_text.lower()
        
        for level, indicators in self.experience_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return level
        
        return "mid"  # Default
    
    def _calculate_industry_match(self, cv_text: str, industry: str) -> float:
        """Calculate how well CV matches target industry"""
        if not industry or industry not in self.industry_keywords:
            return 75
        
        industry_words = self.industry_keywords[industry]
        cv_words = cv_text.lower().split()
        
        matches = sum(1 for word in industry_words if word in cv_words)
        match_percentage = (matches / len(industry_words)) * 100
        
        return min(match_percentage, 100)
    
    def _generate_improvements(self, cv_text: str, job_desc: str) -> List[Dict[str, str]]:
        """Generate specific improvement recommendations"""
        improvements = []
        
        # Check for bullet points
        if not re.search(r'^\s*[-•*]\s', cv_text, re.MULTILINE):
            improvements.append({
                'type': 'formatting',
                'description': 'Use bullet points for better readability',
                'priority': 'high'
            })
        
        # Check for consistent tense
        if re.search(r'\b(ed|ing)\b', cv_text):
            improvements.append({
                'type': 'grammar',
                'description': 'Maintain consistent verb tense throughout',
                'priority': 'medium'
            })
        
        # Check for length
        word_count = len(cv_text.split())
        if word_count > 1000:
            improvements.append({
                'type': 'length',
                'description': 'Consider condensing content to 1-2 pages',
                'priority': 'medium'
            })
        
        return improvements
    
    def _get_industry_suggestions(self, industry: str) -> List[str]:
        """Get industry-specific suggestions"""
        suggestions = {
            'software_engineering': [
                "Include specific technologies and frameworks used",
                "Add GitHub profile link",
                "Mention open source contributions"
            ],
            'data_science': [
                "Include data visualization examples",
                "Mention specific datasets worked with",
                "Add Kaggle competitions or projects"
            ],
            'marketing': [
                "Include campaign metrics and ROI",
                "Add portfolio of marketing materials",
                "Mention specific marketing tools used"
            ]
        }
        
        return suggestions.get(industry, [])
