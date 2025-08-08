#!/usr/bin/env python3
"""
Debug script for cover letter generation issue
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

def test_basic_import():
    """Test basic imports"""
    try:
        from builder.ai_services import EnhancedAICoverLetterService
        print("✅ Successfully imported EnhancedAICoverLetterService")
        return True
    except Exception as e:
        print(f"❌ Failed to import AI service: {str(e)}")
        return False

def test_service_initialization():
    """Test service initialization"""
    try:
        from builder.ai_services import EnhancedAICoverLetterService
        service = EnhancedAICoverLetterService()
        print("✅ Successfully initialized AI service")
        print(f"Client status: {'Available' if service.client else 'Mock mode (no API key)'}")
        return service
    except Exception as e:
        print(f"❌ Failed to initialize AI service: {str(e)}")
        return None

def test_cover_letter_generation(service):
    """Test cover letter generation with minimal data"""
    try:
        # Minimal test data
        cv_insights = {
            'skills': ['Python', 'Django'],
            'experience': ['Software development'],
            'education': ['Computer Science'],
            'achievements': ['Built web applications'],
            'summary': 'Software developer'
        }
        
        job_match = {
            'match_score': 80,
            'matching_skills': ['Python'],
            'missing_skills': ['React'],
            'recommendations': ['Highlight Python skills']
        }
        
        job_title = "Software Developer"
        job_description = "We need a Python developer"
        
        print("🔄 Testing cover letter generation...")
        cover_letter = service.generate_tailored_cover_letter(
            cv_insights, job_match, job_title, job_description
        )
        
        print("✅ Cover letter generated successfully!")
        print(f"Length: {len(cover_letter)} characters")
        print("Preview:")
        print("-" * 40)
        print(cover_letter[:200] + "..." if len(cover_letter) > 200 else cover_letter)
        print("-" * 40)
        return True
        
    except Exception as e:
        print(f"❌ Cover letter generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_environment():
    """Check environment variables"""
    print("🔍 Checking environment...")
    
    # Check for .env file
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                print("✅ OPENAI_API_KEY found in .env file")
            else:
                print("❌ OPENAI_API_KEY not found in .env file")
    else:
        print("❌ .env file not found")
    
    # Check environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OPENAI_API_KEY found in environment (length: {len(api_key)})")
    else:
        print("❌ OPENAI_API_KEY not found in environment")

def main():
    """Main debug function"""
    print("🐛 Cover Letter Generation Debug")
    print("=" * 40)
    
    # Check environment
    check_environment()
    print()
    
    # Test imports
    if not test_basic_import():
        return
    print()
    
    # Test service initialization
    service = test_service_initialization()
    if not service:
        return
    print()
    
    # Test cover letter generation
    test_cover_letter_generation(service)

if __name__ == "__main__":
    main()
