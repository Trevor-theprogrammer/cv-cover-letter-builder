import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_cover_letter_builder.settings')
django.setup()

from builder.models import Template

def add_sample_templates():
    """Add sample CV templates to the database."""
    sample_templates = [
        {
            'name': 'Modern CV',
            'description': 'A clean and modern CV template suitable for tech professionals.',
            'template_content': """
                <div class="cv-template modern">
                    <h1>{{ full_name }}</h1>
                    <p>{{ email }} | {{ phone }} | {{ location }}</p>
                    <h2>Summary</h2>
                    <p>{{ summary }}</p>
                    <h2>Experience</h2>
                    <div class="experience">
                        {{ experience }}
                    </div>
                    <h2>Education</h2>
                    <div class="education">
                        {{ education }}
                    </div>
                    <h2>Skills</h2>
                    <ul class="skills">
                        {{ skills }}
                    </ul>
                </div>
            """,
            'is_default': True,
            'type': 'cv',
            'style': 'modern'
        },
        {
            'name': 'Classic CV',
            'description': 'A traditional and professional CV template.',
            'template_content': """
                <div class="cv-template classic">
                    <h1>{{ full_name }}</h1>
                    <p>{{ email }} | {{ phone }} | {{ location }}</p>
                    <h2>Professional Summary</h2>
                    <p>{{ summary }}</p>
                    <h2>Work Experience</h2>
                    <div class="experience">
                        {{ experience }}
                    </div>
                    <h2>Education</h2>
                    <div class="education">
                        {{ education }}
                    </div>
                    <h2>Skills & Competencies</h2>
                    <ul class="skills">
                        {{ skills }}
                    </ul>
                </div>
            """,
            'is_default': False,
            'type': 'cv',
            'style': 'classic'
        },
        {
            'name': 'Creative CV',
            'description': 'A visually appealing CV template for creative professionals.',
            'template_content': """
                <div class="cv-template creative">
                    <header>
                        <h1>{{ full_name }}</h1>
                        <p>{{ email }} | {{ phone }} | {{ location }}</p>
                    </header>
                    <section>
                        <h2>About Me</h2>
                        <p>{{ summary }}</p>
                    </section>
                    <section>
                        <h2>Experience</h2>
                        <div class="experience">
                            {{ experience }}
                        </div>
                    </section>
                    <section>
                        <h2>Education</h2>
                        <div class="education">
                            {{ education }}
                        </div>
                    </section>
                    <section>
                        <h2>Skills</h2>
                        <div class="skills">
                            {{ skills }}
                        </div>
                    </section>
                </div>
            """,
            'is_default': False,
            'type': 'cv',
            'style': 'creative'
        }
    ]

    for template_data in sample_templates:
        template, created = Template.objects.get_or_create(
            name=template_data['name'],
            defaults=template_data
        )
        if created:
            print(f"Created template: {template.name}")
        else:
            print(f"Template already exists: {template.name}")

if __name__ == '__main__':
    add_sample_templates()
