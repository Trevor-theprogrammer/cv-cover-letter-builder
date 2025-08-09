from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def create_cv(request):
    """View for the CV creation process"""
    templates = [
        {
            'id': 'modern-1',
            'name': 'Modern Professional',
            'description': 'Clean and contemporary design perfect for most industries',
            'preview_image': 'builder/images/templates/modern-1-preview.jpg',
            'badge': 'Popular'
        },
        {
            'id': 'creative-1',
            'name': 'Creative Designer',
            'description': 'Stand out with this bold and innovative layout',
            'preview_image': 'builder/images/templates/creative-1-preview.jpg',
            'badge': 'New'
        },
        {
            'id': 'executive-1',
            'name': 'Executive Suite',
            'description': 'Sophisticated design for senior professionals',
            'preview_image': 'builder/images/templates/executive-1-preview.jpg'
        },
        {
            'id': 'tech-1',
            'name': 'Tech Specialist',
            'description': 'Perfect for IT and tech industry professionals',
            'preview_image': 'builder/images/templates/tech-1-preview.jpg'
        },
        {
            'id': 'minimal-1',
            'name': 'Minimalist',
            'description': 'Simple and elegant design that lets your content shine',
            'preview_image': 'builder/images/templates/minimal-1-preview.jpg'
        },
        {
            'id': 'academic-1',
            'name': 'Academic CV',
            'description': 'Ideal for researchers and educators',
            'preview_image': 'builder/images/templates/academic-1-preview.jpg'
        }
    ]
    
    return render(request, 'builder/create_cv_new.html', {
        'templates': templates
    })
