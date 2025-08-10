from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def create_cv(request):
    """View for the CV creation process"""
    templates = [
        {
            'id': 'modern',
            'name': 'Modern Professional',
            'description': 'Clean and contemporary design perfect for most industries',
            'preview_image': 'builder/images/templates/modern-preview.png',
            'badge': 'Popular'
        },
        {
            'id': 'creative',
            'name': 'Creative Designer',
            'description': 'Stand out with this bold and innovative layout',
            'preview_image': 'builder/images/templates/creative-preview.png',
            'badge': 'New'
        },
        {
            'id': 'minimalist',
            'name': 'Minimalist',
            'description': 'Simple and elegant design that lets your content shine',
            'preview_image': 'builder/images/templates/minimal-preview.png'
        },
        {
            'id': 'tech',
            'name': 'Tech Specialist',
            'description': 'Perfect for IT and tech industry professionals',
            'preview_image': 'builder/images/templates/tech-preview.png'
        },
        {
            'id': 'executive',
            'name': 'Executive Suite',
            'description': 'Sophisticated design for senior professionals',
            'preview_image': 'builder/images/templates/executive-preview.png'
        },
        {
            'id': 'academic',
            'name': 'Academic CV',
            'description': 'Ideal for researchers and educators',
            'preview_image': 'builder/images/templates/academic-preview.png'
        }
    ]
    
    return render(request, 'builder/create_cv_new.html', {
        'templates': templates,
        'selected_template': request.GET.get('template', 'modern')
    })
