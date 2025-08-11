from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Template
import logging

logger = logging.getLogger(__name__)

@login_required
def create_cv(request):
    """View for the CV creation process"""
    logger.info("Accessing create_cv view")
    templates = Template.objects.filter(type='cv').order_by('name')
    user_data = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        # Add any other saved user data here
    }
    return render(request, 'builder/create_cv.html', {
        'templates': templates,
        'user_data': user_data,
        'selected_template': request.GET.get('template', 'modern')
    })
