# CV & Cover Letter Builder

A comprehensive Django web application for creating professional CVs and generating AI-powered cover letters.

## Features

- **CV Creation**: Build professional CVs with customizable sections
- **AI-Powered Cover Letters**: Generate personalized cover letters using OpenAI GPT-4
- **CV Analysis**: Analyze your CV for strengths, improvements, and ATS compatibility
- **File Upload**: Upload existing CVs (PDF/DOCX) for analysis and processing
- **Templates**: Browse and use professional CV templates
- **User Management**: Secure user registration and authentication
- **Responsive Design**: Mobile-friendly interface

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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
   ```
   Edit `.env` file with your actual API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key
   SECRET_KEY=your-django-secret-key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and go to: http://127.0.0.1:8000

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional - for AWS S3 storage
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

## Usage

### For Users
1. **Register/Login**: Create an account or log in
2. **Create CV**: Build a new CV from scratch
3. **Upload CV**: Upload existing PDF/DOCX files for analysis
4. **Generate Cover Letters**: Use AI to create personalized cover letters
5. **Analyze CV**: Get detailed feedback on your CV
6. **Browse Templates**: Use professional templates

### For Developers
- **Admin Panel**: Access Django admin at `/admin/`
- **Database**: SQLite by default (configurable for production)
- **Static Files**: Served from `/static/` directory
- **Media Files**: Stored in `/media/` directory (local) or S3 (production)

## Project Structure

```
cv-cover-letter-builder/
├── builder/                 # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Django forms
│   ├── urls.py             # URL patterns
│   ├── ai_services.py      # OpenAI integration
│   ├── file_handlers.py    # File processing utilities
│   └── cv_analyzer.py      # CV analysis logic
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # Uploaded files
├── core/                   # Django project settings
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## API Endpoints

- `/` - Home page
- `/accounts/` - Authentication (login/register)
- `/dashboard/` - User dashboard
- `/create/` - Create new CV
- `/upload/` - Upload CV files
- `/generate-letter/` - Generate cover letters
- `/analyze/` - CV analysis
- `/templates/` - CV templates
- `/admin/` - Django admin panel

## Testing

Run the test suite:
```bash
python manage.py test
```

## Production Deployment

1. **Set DEBUG=False** in settings
2. **Configure production database** (PostgreSQL recommended)
3. **Set up proper static file serving** (WhiteNoise or CDN)
4. **Configure HTTPS** and security headers
5. **Set up proper logging**
6. **Use environment variables** for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is open source and available under the MIT License.
