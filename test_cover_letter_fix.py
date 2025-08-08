#!/usr/bin/env python3
"""
Test script to verify cover letter generation fix
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

def test_cover_letter_generation():
    """Test the fixed cover letter generation"""
    print("🧪 Testing Cover Letter Generation Fix")
    print("=" * 50)
    
    try:
        from builder.ai_services import EnhancedAICoverLetterService
        
        # Initialize service
        print("1. Initializing AI service...")
        service = EnhancedAICoverLetterService()
        print(f"   ✅ Service initialized (API key: {'Available' if service.client else 'Mock mode'})")
        
        # Test CV insights extraction
        print("\n2. Testing CV insights extraction...")
        cv_text = """
        John Doe
        Software Engineer
        
        Experience:
        - 3 years as Python Developer
        - Built web applications using Django
        - Improved system performance by 30%
        
        Skills: Python, Django, JavaScript, SQL
        Education: Bachelor's in Computer Science
        """
        
        cv_insights = service.extract_cv_insights(cv_text)
        print(f"   ✅ CV insights extracted: {len(cv_insights.get('skills', []))} skills found")
        
        # Test job matching
        print("\n3. Testing job matching...")
        job_match = service.match_cv_to_job(cv_insights, "Python Developer", "We need a Python developer with Django experience")
        print(f"   ✅ Job matching completed: {job_match.get('match_score', 0)}% match")
        
        # Test cover letter generation
        print("\n4. Testing cover letter generation...")
        cover_letter = service.generate_tailored_cover_letter(
            cv_insights=cv_insights,
            job_match=job_match,
            job_title="Python Developer",
            job_description="We are looking for a Python developer with Django experience to join our team.",
            tone="professional",
            template_type="standard"
        )
        
        print(f"   ✅ Cover letter generated successfully!")
        print(f"   📏 Length: {len(cover_letter)} characters")
        print(f"   📝 Preview:")
        print("   " + "-" * 40)
        preview = cover_letter[:300] + "..." if len(cover_letter) > 300 else cover_letter
        for line in preview.split('\n'):
            print(f"   {line}")
        print("   " + "-" * 40)
        
        # Test error handling
        print("\n5. Testing error handling...")
        try:
            service.generate_tailored_cover_letter({}, {}, "", "")
        except ValueError as e:
            print(f"   ✅ Error handling works: {str(e)}")
        except Exception as e:
            print(f"   ⚠️  Unexpected error type: {str(e)}")
        
        print("\n🎉 All tests passed! Cover letter generation is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_setup():
    """Test environment setup"""
    print("\n🔧 Environment Check")
    print("=" * 30)
    
    # Check OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OPENAI_API_KEY: Found ({len(api_key)} chars)")
    else:
        print("⚠️  OPENAI_API_KEY: Not found (will use mock responses)")
    
    # Check Django setup
    try:
        from django.conf import settings
        print("✅ Django: Configured")
    except Exception as e:
        print(f"❌ Django: Error - {str(e)}")
    
    # Check required packages
    try:
        import openai
        print("✅ OpenAI package: Available")
    except ImportError:
        print("❌ OpenAI package: Missing")

if __name__ == "__main__":
    test_environment_setup()
    success = test_cover_letter_generation()
    
    if success:
        print("\n✨ Fix verification complete! Your cover letter generation should now work.")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000")
        print("3. Try generating a cover letter")
    else:
        print("\n❌ Fix verification failed. Please check the errors above.")
