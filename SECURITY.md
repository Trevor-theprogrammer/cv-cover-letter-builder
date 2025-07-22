# Security Guidelines

## API Key Management

### 1. Environment Variables

Always store sensitive API keys in environment variables:

```bash
# Create .env file
cp .env.example .env

# Add your API key
echo "OPENAI_API_KEY=your_actual_key_here" >> .env
```

### 2. Never Commit Secrets

- **DO NOT** commit `.env` files to version control
- **DO NOT** hardcode API keys in source code
- **DO NOT** push secrets to GitHub

### 3. Git Protection

The `.gitignore` file already includes:

- `.env` files
- API key patterns
- Local settings

### 4. Environment Setup

```bash
# Install python-decouple for environment variable management
pip install python-decouple

# Update settings.py to use environment variables
```

### 5. Key Rotation

If you accidentally exposed a key:

1. **Immediately revoke** the key in your OpenAI dashboard
2. **Generate a new key**
3. **Update your .env file**
4. **Restart the application**

### 6. Development Setup

```bash
# 1. Copy example environment file
cp .env.example .env

# 2. Edit .env with your actual keys
nano .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python manage.py runserver
```

### 7. Production Deployment

- Use environment variables in production
- Consider using services like AWS Secrets Manager or Azure Key Vault
- Set up automated secret scanning in CI/CD

### 8. Security Checklist

- [ ] No hardcoded secrets in source code
- [ ] .env file in .gitignore
- [ ] Environment variables properly configured
- [ ] API keys rotated regularly
- [ ] Secret scanning enabled in CI/CD

## Quick Fix Commands

```bash
# Check for secrets in git history
git log --all --grep='api_key\|secret\|password'

# Remove sensitive files from git history
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch .env' HEAD

# Add .env to .gitignore if not already present
echo ".env" >> .gitignore
```
