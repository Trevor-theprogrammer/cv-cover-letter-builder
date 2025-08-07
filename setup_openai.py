#!/usr/bin/env python3
"""
OpenAI API Setup Script for CV Cover Letter Builder
This script helps you set up and test your OpenAI API key.
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

def check_env_file():
    """Check if .env file exists and has OPENAI_API_KEY"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Creating .env file from .env.example...")
        
        # Copy from .env.example if it exists
        example_path = Path('.env.example')
        if example_path.exists():
            with open(example_path, 'r') as example_file:
                content = example_file.read()
            with open(env_path, 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created from .env.example")
        else:
            # Create basic .env file
            with open(env_path, 'w') as env_file:
                env_file.write("# Django Settings\n")
                env_file.write("SECRET_KEY=your-secret-key-here\n")
                env_file.write("DEBUG=True\n")
                env_file.write("ALLOWED_HOSTS=localhost,127.0.0.1\n\n")
                env_file.write("# OpenAI API Key\n")
                env_file.write("OPENAI_API_KEY=your-openai-api-key-here\n")
            print("✅ Basic .env file created")
    
    # Check if OPENAI_API_KEY is set
    with open(env_path, 'r') as env_file:
        content = env_file.read()
        
    if 'OPENAI_API_KEY=your-openai-api-key-here' in content or 'OPENAI_API_KEY=' in content:
        print("⚠️  OPENAI_API_KEY not configured in .env file")
        return False
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            return False
        
        if api_key == 'your-openai-api-key-here':
            print("❌ OPENAI_API_KEY is still set to placeholder value")
            return False
        
        # Test API connection
        client = OpenAI(api_key=api_key)
        
        print("🔄 Testing OpenAI API connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! This is a test message."}],
            max_tokens=10
        )
        
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 OpenAI API Setup for CV Cover Letter Builder")
    print("=" * 50)
    
    # Step 1: Check .env file
    print("\n1. Checking .env file...")
    env_configured = check_env_file()
    
    if not env_configured:
        print("\n📝 Please follow these steps:")
        print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
        print("2. Open the .env file in your project root")
        print("3. Replace 'your-openai-api-key-here' with your actual API key")
        print("4. Run this script again to test the connection")
        return
    
    # Step 2: Test API connection
    print("\n2. Testing OpenAI API connection...")
    if test_openai_connection():
        print("\n🎉 Setup complete! Your OpenAI API is ready to use.")
        print("\nNext steps:")
        print("- Run: python manage.py runserver")
        print("- Visit: http://localhost:8000")
        print("- Test the AI cover letter generation features")
    else:
        print("\n❌ Setup incomplete. Please check your API key and try again.")

if __name__ == "__main__":
    main()
