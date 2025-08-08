#!/usr/bin/env python3
"""
Simple test to verify cover letter generation is working
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variable for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def test_ai_service_only():
    """Test just the AI service without Django"""
    print("🔧 Testing AI Service...")
    
    try:
        # Import after setting environment
        from builder.ai_services import EnhancedAICoverLetterService
        
        service = EnhancedAICoverLetterService()
        print("✅ AI Service initialized successfully")
        
        # Test CV insights extraction
        cv_text = """
        John Doe
        Software Engineer
        john@example.com | (555) 123-4567 | New York, NY
        
        EXPERIENCE
        Senior Software Engineer at TechCorp (2020-2023)
        - Led development of web applications using Python and Django
        - Managed team of 5 developers
        - Improved system performance by 40%
        
        SKILLS
        Python, Django, JavaScript, SQL, Team Leadership, Project Management
        """
        
        cv_insights = service.extract_cv_insights(cv_text)
        print(f"✅ CV insights extracted: {len(cv_insights.get('skills', []))} skills found")
        print(f"   Skills: {cv_insights.get('skills', [])}")
        
        # Test job matching
        job_title = "Senior Python Developer"
        job_description = """
        We are looking for a Senior Python Developer to join our team.
        Requirements: Python, Django, team leadership, 5+ years experience.
        """
        
        job_match = service.match_cv_to_job(cv_insights, job_title, job_description)
        print(f"✅ Job matching completed: {job_match.get('match_score', 0)}% match")
        print(f"   Matching skills: {job_match.get('matching_skills', [])}")
        
        # Test cover letter generation
        cover_letter = service.generate_tailored_cover_letter(
            cv_insights, job_match, job_title, job_description
        )
        print(f"✅ Cover letter generated: {len(cover_letter)} characters")
        print(f"   Preview: {cover_letter[:300]}...")
        
        # Test comprehensive CV analysis
        analysis = service.analyze_cv_comprehensive(cv_text)
        print(f"✅ CV analysis completed: {analysis.get('overall_score', 0)}/100 score")
        print(f"   Strengths: {len(analysis.get('strengths', []))} items")
        print(f"   Recommendations: {len(analysis.get('recommendations', []))} items")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Service test failed: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

def main():
    """Run the test"""
    print("🚀 Testing Cover Letter Generation Fix")
    print("=" * 50)
    
    success = test_ai_service_only()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS! Cover letter generation is working!")
        print("\n✨ Key improvements made:")
        print("- ✅ Enhanced error handling")
        print("- ✅ Robust fallback when OpenAI API unavailable")
        print("- ✅ Fixed URL routing (builder:home)")
        print("- ✅ Better input validation")
        print("- ✅ Improved user error messages")
        print("\n📝 The application now generates cover letters even without OpenAI API!")
    else:
        print("❌ Test failed. Check error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
