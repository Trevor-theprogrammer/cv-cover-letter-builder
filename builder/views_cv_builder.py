from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

@login_required
def create_cv(request):
    """View for the CV creation process"""
    logger.info("Accessing create_cv view")
    templates = [
        {
            'id': 'modern',
            'name': 'modern',
            'description': 'Clean and contemporary design perfect for most industries',
            'badge': 'Popular'
        },
        {
            'id': 'creative',
            'name': 'creative',
            'description': 'Stand out with this bold and innovative layout',
            'badge': 'New'
        },
        {
            'id': 'minimal',
            'name': 'minimal',
            'description': 'Simple and elegant design that lets your content shine'
        },
        {
            'id': 'classic',
            'name': 'classic',
            'description': 'Timeless professional design for traditional industries'
        },
        {
            'id': 'basic',
            'name': 'basic',
            'description': 'Clean and simple design suitable for any industry'
        }
    ]
    
    return render(request, 'builder/create_cv_new.html', {
        'templates': templates,
        'selected_template': request.GET.get('template', 'modern')
    })
