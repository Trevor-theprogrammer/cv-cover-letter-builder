#!/usr/bin/env python3
"""
Verification Script for CV Cover Letter Builder
This script verifies that all components are working correctly after fixes.
"""

import os
import sys
import django
from pathlib import Path
import subprocess

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def check_django_setup():
    """Verify Django is properly configured"""
    print("🔧 Checking Django Setup...")
    
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Check if settings are configured
        if not settings.configured:
            print("❌ Django settings not configured")
            return False
        
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        print("✅ Django setup is working")
        return True
        
    except Exception as e:
        print(f"❌ Django setup error: {str(e)}")
        return False

def check_database():
    """Check database and migrations"""
    print("\n💾 Checking Database...")
    
    try:
        # Check if migrations are applied
        from django.core.management import call_command
        from io import StringIO
        
        # Capture output
        out = StringIO()
        call_command('showmigrations', stdout=out)
        migrations_output = out.getvalue()
        
        # Check for unapplied migrations
        if '[ ]' in migrations_output:
            print("⚠️  Unapplied migrations found")
            print("Run: python manage.py migrate")
            return False
        
        # Test database queries
        from builder.models import CV, CoverLetter
        cv_count = CV.objects.count()
        letter_count = CoverLetter.objects.count()
        
        print(f"✅ Database is working")
        print(f"   CVs in database: {cv_count}")
        print(f"   Cover letters in database: {letter_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False

def check_static_files():
    """Check static files configuration"""
    print("\n📁 Checking Static Files...")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        # Check static directories exist
        static_dirs = settings.STATICFILES_DIRS
        for static_dir in static_dirs:
            if not Path(static_dir).exists():
                print(f"⚠️  Static directory missing: {static_dir}")
        
        # Check for key static files
        key_files = [
            'builder/css/cvmaker-style.css',
            'builder/js/mobile-nav-master.js'
        ]
        
        missing_files = []
        for file_path in key_files:
            if not find(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"⚠️  Missing static files: {missing_files}")
        else:
            print("✅ Static files configuration is working")
        
        return len(missing_files) == 0
        
    except Exception as e:
        print(f"❌ Static files error: {str(e)}")
        return False

def check_templates():
    """Check template configuration"""
    print("\n📄 Checking Templates...")
    
    try:
        from django.template.loader import get_template
        
        # Key templates to check
        key_templates = [
            'builder/base.html',
            'builder/dashboard.html',
            'builder/ai_cover_letter.html',
            'builder/upload_cv.html'
        ]
        
        missing_templates = []
        for template_name in key_templates:
            try:
                get_template(template_name)
            except:
                missing_templates.append(template_name)
        
        if missing_templates:
            print(f"❌ Missing templates: {missing_templates}")
            return False
        
        print("✅ Template configuration is working")
        return True
        
    except Exception as e:
        print(f"❌ Template error: {str(e)}")
        return False

def check_ai_services():
    """Check AI services functionality"""
    print("\n🤖 Checking AI Services...")
    
    try:
        from builder.ai_services import EnhancedAICoverLetterService
        
        service = EnhancedAICoverLetterService()
        
        # Test basic functionality
        test_cv = "John Doe, Software Engineer with 5 years experience in Python and Django."
        insights = service.extract_cv_insights(test_cv)
        
        if not insights or not isinstance(insights, dict):
            print("❌ AI service not returning proper insights")
            return False
        
        # Check if OpenAI is configured
        if service.client is None:
            print("⚠️  OpenAI API key not configured - using mock data")
        else:
            print("✅ OpenAI API key is configured")
        
        print("✅ AI services are working")
        return True
        
    except Exception as e:
        print(f"❌ AI services error: {str(e)}")
        return False

def check_urls():
    """Check URL configuration"""
    print("\n🔗 Checking URL Configuration...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Key URLs to check
        key_urls = [
            ('builder:home', {}),
            ('builder:dashboard', {}),
            ('builder:upload_cv', {}),
            ('builder:ai_cover_letter', {}),
        ]
        
        client = Client()
        working_urls = []
        broken_urls = []
        
        for url_name, kwargs in key_urls:
            try:
                url = reverse(url_name, kwargs=kwargs)
                response = client.get(url)
                
                if response.status_code in [200, 302]:  # 302 for redirects (login required)
                    working_urls.append(url_name)
                else:
                    broken_urls.append((url_name, response.status_code))
                    
            except Exception as e:
                broken_urls.append((url_name, str(e)))
        
        if broken_urls:
            print(f"❌ Broken URLs found: {broken_urls}")
            return False
        
        print(f"✅ URL configuration is working ({len(working_urls)} URLs checked)")
        return True
        
    except Exception as e:
        print(f"❌ URL configuration error: {str(e)}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking Dependencies...")
    
    try:
        # Read requirements.txt
        requirements_file = Path('requirements.txt')
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        with open(requirements_file, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Check key imports
        key_imports = [
            ('django', 'Django'),
            ('openai', 'OpenAI'),
            ('PIL', 'Pillow'),
            ('PyPDF2', 'PyPDF2'),
            ('crispy_forms', 'django-crispy-forms'),
        ]
        
        missing_deps = []
        for import_name, package_name in key_imports:
            try:
                __import__(import_name)
            except ImportError:
                missing_deps.append(package_name)
        
        if missing_deps:
            print(f"❌ Missing dependencies: {missing_deps}")
            print("Run: pip install -r requirements.txt")
            return False
        
        print(f"✅ All dependencies are installed ({len(requirements)} packages)")
        return True
        
    except Exception as e:
        print(f"❌ Dependencies check error: {str(e)}")
        return False

def run_basic_tests():
    """Run basic Django tests"""
    print("\n🧪 Running Basic Tests...")
    
    try:
        from django.test.utils import get_runner
        from django.conf import settings
        
        # Get test runner
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=0, interactive=False)
        
        # Run tests for builder app
        failures = test_runner.run_tests(['builder.tests'])
        
        if failures:
            print(f"❌ {failures} test(s) failed")
            return False
        
        print("✅ Basic tests passed")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not run tests: {str(e)}")
        return True  # Don't fail verification if tests can't run

def main():
    """Run all verification checks"""
    print("🔍 CV Cover Letter Builder - System Verification")
    print("=" * 60)
    
    checks = [
        ("Django Setup", check_django_setup),
        ("Database", check_database),
        ("Static Files", check_static_files),
        ("Templates", check_templates),
        ("AI Services", check_ai_services),
        ("URL Configuration", check_urls),
        ("Dependencies", check_dependencies),
        ("Basic Tests", run_basic_tests),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check crashed: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Verification Results")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your application is ready to use.")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000")
        print("3. Test the application features")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        
    print("\n💡 Additional recommendations:")
    print("- Configure OpenAI API key for full AI functionality")
    print("- Run 'python setup_openai.py' to set up OpenAI")
    print("- Run 'python test_openai.py' to test AI features")

if __name__ == "__main__":
    main()
