from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import json

@login_required
def template_preview(request, template_id):
    """Render a preview of the selected CV template"""
    
    # Sample data for preview
    sample_data = {
        'name': 'John Smith',
        'title': 'Senior Software Engineer',
        'contact': {
            'email': 'john.smith@email.com',
            'phone': '+1 (555) 123-4567',
            'location': 'San Francisco, CA'
        },
        'summary': 'Experienced software engineer with 8+ years of expertise in full-stack development...',
        'experience': [
            {
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'period': '2020 - Present',
                'description': [
                    'Led development of cloud-native microservices architecture',
                    'Managed team of 5 developers for critical projects',
                    'Reduced system downtime by 40% through improved monitoring'
                ]
            }
        ],
        'education': [
            {
                'degree': 'Master of Computer Science',
                'school': 'Stanford University',
                'year': '2015'
            }
        ],
        'skills': [
            'Python', 'JavaScript', 'React', 'Node.js', 'AWS',
            'Docker', 'Kubernetes', 'CI/CD', 'System Design'
        ]
    }
    
    # In a real application, we would have different template files for each template_id
    template_path = f'builder/templates/{template_id}.html'
    
    try:
        html_content = render_to_string(template_path, {'cv': sample_data})
        return HttpResponse(html_content)
    except Exception as e:
        return HttpResponse(
            'Template preview not available',
            status=404
        )
