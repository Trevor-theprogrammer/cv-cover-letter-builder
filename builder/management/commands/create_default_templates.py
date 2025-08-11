from django.core.management.base import BaseCommand
from builder.models import Template
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Creates default CV templates'

    def handle(self, *args, **kwargs):
        templates = [
            {
                'name': 'Modern Professional',
                'style': 'modern',
                'description': 'Clean and contemporary design perfect for most industries',
                'template_content': '<!-- Your template HTML here -->',
                'is_default': True,
                'type': 'cv',
                'preview_image': 'modern_preview.jpg'
            },
            {
                'name': 'Creative Portfolio',
                'style': 'creative',
                'description': 'Stand out with this bold and innovative layout',
                'template_content': '<!-- Your template HTML here -->',
                'is_default': True,
                'type': 'cv',
                'preview_image': 'creative_preview.jpg'
            },
            # Add more templates as needed
        ]

        for template_data in templates:
            preview_image = template_data.pop('preview_image')
            template, created = Template.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            
            if created:
                # Load preview image if it exists
                image_path = os.path.join(settings.BASE_DIR, 'static', 'builder', 'images', 'templates', preview_image)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        template.preview_image.save(preview_image, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created template: {template.name}'))
