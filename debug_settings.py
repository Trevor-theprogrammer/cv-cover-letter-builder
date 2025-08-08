#!/usr/bin/env python
"""
Debug script to check Django settings configuration
"""
import os
import sys
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    import django
    from django.conf import settings
    
    print("=== Django Settings Debug ===")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"SECRET_KEY set: {'Yes' if settings.SECRET_KEY else 'No'}")
    
    # Check environment variables
    print("\n=== Environment Variables ===")
    print(f"DEBUG env var: {os.environ.get('DEBUG', 'Not set')}")
    print(f"ALLOWED_HOSTS env var: {os.environ.get('ALLOWED_HOSTS', 'Not set')}")
    print(f"SECRET_KEY env var: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")
    print(f"DATABASE_URL env var: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
    
except Exception as e:
    print(f"Error loading Django settings: {e}")
    import traceback
    traceback.print_exc()
