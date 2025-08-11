from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Template, CV
import logging

logger = logging.getLogger(__name__)

@login_required
def create_cv(request):
    """View for the CV creation process"""
    logger.info("Accessing create_cv view")
    
    if request.method == 'POST':
        # Handle form submission
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        summary = request.POST.get('summary', '')
        phone = request.POST.get('phone', '')
        location = request.POST.get('location', '')
        template_id = request.POST.get('template_id')
        
        if not all([full_name, email, template_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('builder:create_cv')
        
        try:
            template = Template.objects.get(id=template_id, type='cv')
            
            # Create new CV instance
            cv = CV.objects.create(
                title=f"{full_name}'s CV",
                user=request.user
            )
            
            # Store initial data in session for next steps
            request.session['cv_data'] = {
                'full_name': full_name,
                'email': email,
                'summary': summary,
                'phone': phone,
                'location': location,
                'template_id': template_id
            }
            
            logger.info(f"CV created successfully for user {request.user.username}")
            messages.success(request, 'CV created successfully!')
            return redirect('builder:cv_detail', pk=cv.pk)
            
        except Template.DoesNotExist:
            messages.error(request, 'Invalid template selected.')
            return redirect('builder:create_cv')
        except Exception as e:
            logger.error(f"Error creating CV: {str(e)}")
            messages.error(request, 'An error occurred while creating your CV. Please try again.')
            return redirect('builder:create_cv')
    
    # Handle GET request
    templates = Template.objects.filter(type='cv').order_by('name')
    user_data = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        'summary': '',
        'phone': '',
        'location': ''
    }
    
    return render(request, 'builder/create_cv.html', {
        'templates': templates,
        'user_data': user_data,
        'selected_template': request.GET.get('template', 'modern')
    })
