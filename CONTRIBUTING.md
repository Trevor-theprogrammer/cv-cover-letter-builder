# Contributing to CV & Cover Letter Builder

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the CV & Cover Letter Builder.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Docker (optional, for containerized development)

### Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/your-username/cv-cover-letter-builder.git
   cd cv-cover-letter-builder
   ```

2. **Create virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Development Workflow

### Branch Naming

- `feature/description` - new features
- `bugfix/description` - bug fixes
- `hotfix/description` - urgent fixes
- `docs/description` - documentation updates

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Run tests with: `python manage.py test`

### Commit Messages

Use conventional commits format:

- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `style: format code`
- `refactor: restructure code`
- `test: add tests`

## Pull Request Process

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**

   ```bash
   python manage.py test
   python manage.py check
   ```

4. **Commit and push**

   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use the PR template
   - Provide clear description of changes
   - Link any related issues

## Code Guidelines

### Python Code

- Use type hints where appropriate
- Follow PEP 8 style guide
- Maximum line length: 88 characters (Black formatter)
- Use f-strings for string formatting

### Django Best Practices

- Use Django's built-in features when possible
- Follow Django's security best practices
- Use migrations for database changes
- Optimize database queries

### Frontend

- Use semantic HTML
- Ensure responsive design
- Test on multiple browsers
- Follow accessibility guidelines (WCAG 2.1)

## Testing Guidelines

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test builder.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

- Test both success and failure cases
- Use descriptive test names
- Mock external API calls
- Test edge cases

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include examples in docstrings
- Update README.md for new features

### API Documentation

- Document all API endpoints
- Include request/response examples
- Update OpenAPI/Swagger documentation

## Issue Reporting

### Bug Reports

Include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Feature Requests

Include:

- Clear description of the feature
- Use case and motivation
- Possible implementation approach
- Acceptance criteria

## Security

- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Follow OWASP guidelines
- Report security issues privately

## Getting Help

- Check existing issues and documentation
- Join our community discussions
- Contact maintainers for questions

## Recognition

Contributors will be recognized in:

- README.md contributors section
- CHANGELOG.md
- Release notes

Thank you for contributing!
