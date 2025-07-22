#!/usr/bin/env python
"""
Security setup script for CV Cover Letter Builder
This script helps users set up their environment securely
"""

import os
import sys
from pathlib import Path

def setup_security():
    """Set up secure environment configuration"""
    base_dir = Path(__file__).parent
    
    # Check if .env exists
    env_file = base_dir / '.env'
    example_env = base_dir / '.env.example'
    
    if not env_file.exists():
        print("🔐 Setting up secure environment...")
        
        # Copy example file
        if example_env.exists():
            with open(example_env, 'r') as f:
                content = f.read()
            
            # Create .env file
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from .env.example")
            print("📋 Please edit .env file and add your actual API keys")
            print("🚨 Remember to NEVER commit .env to version control!")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")
    
    # Check if .env is in .gitignore
    gitignore = base_dir / '.gitignore'
    if gitignore.exists():
        with open(gitignore, 'r') as f:
            content = f.read()
        
        if '.env' not in content:
            with open(gitignore, 'a') as f:
                f.write('\n# Environment variables\n.env\n.env.*\n')
            print("✅ Added .env to .gitignore")
        else:
            print("✅ .env already in .gitignore")
    
    print("\n🛡️ Security Setup Complete!")
    print("Next steps:")
    print("1. Edit .env file with your actual API keys")
    print("2. Run: python manage.py runserver")
    print("3. Never commit .env to git!")

if __name__ == "__main__":
    setup_security()
