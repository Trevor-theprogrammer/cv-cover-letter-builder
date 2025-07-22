# AGENT.md - CV & Cover Letter Builder

## Build/Test Commands
- `make test` - Run all Django tests
- `python manage.py test builder.tests.test_views.TestSpecificView` - Run single test
- `make lint` - Run flake8 linting
- `make format` - Format code with black (line length 88)
- `make migrate` - Run database migrations
- `make runserver` - Start development server

## Architecture
- **Django 4.x** web application with SQLite database
- **Core apps**: `core/` (settings, URLs), `builder/` (main app)
- **Key models**: CV, CVSection, CoverLetter (in `builder/models.py`)
- **AI integration**: OpenAI GPT-4 for cover letter generation (`builder/ai_services.py`)
- **File handling**: PDF/DOCX upload support (`builder/file_handlers.py`)
- **Templates**: Bootstrap-based responsive UI in `templates/`

## Code Style
- **Formatting**: Black with 88 character line length
- **Imports**: Django imports first, then third-party, then local
- **Naming**: Snake_case for variables/functions, PascalCase for classes
- **Models**: Use descriptive names, include `__str__` methods, add timestamps
- **Views**: Class-based views preferred, use Django forms for validation
- **Error handling**: Use Django's built-in error handling and logging
