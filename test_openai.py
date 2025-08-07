#!/usr/bin/env python3
"""
OpenAI API Test Script for CV Cover Letter Builder
This script tests all AI functionality in your application.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from builder.ai_services import EnhancedAICoverLetterService

def test_cv_insights():
    """Test CV insights extraction"""
    print("🔍 Testing CV Insights Extraction...")
    
    service = EnhancedAICoverLetterService()
    
    # Sample CV text for testing
    sample_cv = """
    John Doe
    Software Engineer
    
    Experience:
    - 5 years as Full Stack Developer at TechCorp
    - Led team of 8 developers on e-commerce platform
    - Reduced page load time by 40% through optimization
    - Increased user engagement by 25%
    
    Skills:
    Python, Django, JavaScript, React, SQL, AWS, Docker
    
    Education:
    Bachelor of Science in Computer Science, MIT, 2018
    
    Achievements:
    - AWS Certified Solutions Architect
    - Published 3 technical articles
    - Speaker at 2 tech conferences
    """
    
    try:
        insights = service.extract_cv_insights(sample_cv)
        
        print("✅ CV Insights extracted successfully!")
        print(f"Skills found: {len(insights.get('skills', []))}")
        print(f"Experience points: {len(insights.get('experience', []))}")
        print(f"Achievements: {len(insights.get('achievements', []))}")
        print(f"Summary: {insights.get('summary', 'N/A')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ CV Insights extraction failed: {str(e)}")
        return False

def test_job_matching():
    """Test CV to job matching"""
    print("\n🎯 Testing Job Matching...")
    
    service = EnhancedAICoverLetterService()
    
    # Sample data
    cv_insights = {
        'skills': ['Python', 'Django', 'JavaScript', 'SQL', 'Team Leadership'],
        'experience': ['5+ years software development', '3 years team lead'],
        'education': ["Bachelor's in Computer Science"],
        'achievements': ['Led team of 5 developers', 'Reduced load time by 40%'],
        'summary': 'Experienced full-stack developer'
    }
    
    job_title = "Senior Full Stack Developer"
    job_description = """
    We are looking for a Senior Full Stack Developer with 5+ years experience.
    Required skills: Python, Django, JavaScript, React, SQL, AWS.
    Leadership experience preferred.
    """
    
    try:
        match_result = service.match_cv_to_job(cv_insights, job_title, job_description)
        
        print("✅ Job matching completed successfully!")
        print(f"Match Score: {match_result.get('match_score', 0)}%")
        print(f"Matching Skills: {len(match_result.get('matching_skills', []))}")
        print(f"Missing Skills: {len(match_result.get('missing_skills', []))}")
        print(f"Recommendations: {len(match_result.get('recommendations', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Job matching failed: {str(e)}")
        return False

def test_cover_letter_generation():
    """Test cover letter generation"""
    print("\n📝 Testing Cover Letter Generation...")
    
    service = EnhancedAICoverLetterService()
    
    # Sample data
    cv_insights = {
        'skills': ['Python', 'Django', 'JavaScript', 'SQL', 'Team Leadership'],
        'experience': ['5+ years software development', '3 years team lead'],
        'education': ["Bachelor's in Computer Science"],
        'achievements': ['Led team of 5 developers', 'Reduced load time by 40%', 'Increased efficiency by 25%'],
        'summary': 'Experienced full-stack developer with strong backend skills'
    }
    
    job_match = {
        'match_score': 85,
        'matching_skills': ['Python', 'Django', 'Team Leadership'],
        'missing_skills': ['React', 'AWS'],
        'recommendations': ['Highlight leadership experience']
    }
    
    job_title = "Senior Full Stack Developer"
    job_description = "We need an experienced developer with Python and Django skills."
    
    try:
        cover_letter = service.generate_tailored_cover_letter(
            cv_insights, job_match, job_title, job_description
        )
        
        print("✅ Cover letter generated successfully!")
        print(f"Length: {len(cover_letter)} characters")
        print("Preview:")
        print("-" * 40)
        print(cover_letter[:300] + "..." if len(cover_letter) > 300 else cover_letter)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Cover letter generation failed: {str(e)}")
        return False

def test_comprehensive_analysis():
    """Test comprehensive CV analysis"""
    print("\n📊 Testing Comprehensive CV Analysis...")
    
    service = EnhancedAICoverLetterService()
    
    sample_cv = """
    Jane Smith
    Senior Data Scientist
    
    Professional Summary:
    Experienced data scientist with 7+ years in machine learning and analytics.
    
    Experience:
    - Senior Data Scientist at DataCorp (2020-2024)
    - Built ML models that increased revenue by 30%
    - Led data science team of 6 members
    - Implemented automated reporting systems
    
    Skills:
    Python, R, SQL, TensorFlow, PyTorch, AWS, Docker, Kubernetes
    
    Education:
    PhD in Statistics, Stanford University, 2017
    MS in Computer Science, UC Berkeley, 2015
    """
    
    try:
        analysis = service.analyze_cv_comprehensive(sample_cv)
        
        print("✅ Comprehensive analysis completed!")
        print(f"Overall Score: {analysis.get('overall_score', 0)}/100")
        print(f"ATS Score: {analysis.get('ats_score', 0)}/100")
        print(f"Keyword Score: {analysis.get('keyword_score', 0)}/100")
        print(f"Strengths: {len(analysis.get('strengths', []))}")
        print(f"Weaknesses: {len(analysis.get('weaknesses', []))}")
        print(f"Recommendations: {len(analysis.get('recommendations', []))}")
        print(f"Experience Level: {analysis.get('experience_level', 'N/A')}")
        print(f"Industry: {analysis.get('industry', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive analysis failed: {str(e)}")
        return False

def check_api_key():
    """Check if OpenAI API key is configured"""
    print("🔑 Checking OpenAI API Key Configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False
        
        if api_key == 'your-openai-api-key-here':
            print("❌ OPENAI_API_KEY is still set to placeholder")
            return False
        
        if len(api_key) < 20:
            print("❌ OPENAI_API_KEY appears to be invalid (too short)")
            return False
        
        print("✅ OpenAI API Key is configured")
        print(f"Key length: {len(api_key)} characters")
        print(f"Key preview: {api_key[:8]}...{api_key[-4:]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking API key: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 OpenAI AI Services Test Suite")
    print("=" * 50)
    
    # Check API key first
    api_key_ok = check_api_key()
    
    if not api_key_ok:
        print("\n⚠️  API key not configured. Tests will use mock data.")
        print("Run 'python setup_openai.py' to configure your API key.")
    
    print("\n" + "=" * 50)
    
    # Run tests
    tests = [
        ("CV Insights Extraction", test_cv_insights),
        ("Job Matching", test_job_matching),
        ("Cover Letter Generation", test_cover_letter_generation),
        ("Comprehensive Analysis", test_comprehensive_analysis),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI services are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    if not api_key_ok:
        print("\n💡 Note: Configure your OpenAI API key for full functionality.")

if __name__ == "__main__":
    main()
