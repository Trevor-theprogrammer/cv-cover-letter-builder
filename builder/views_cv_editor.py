from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import CV

@login_required
def edit_cv_template(request, template_id):
    """View for editing a CV with a specific template"""
    # Get or create CV instance
    cv, created = CV.objects.get_or_create(
        user=request.user,
        template_id=template_id
    )
    
    return render(request, 'builder/edit_cv.html', {
        'cv': cv,
        'template_id': template_id
    })

@login_required
@require_http_methods(["POST"])
def save_cv_draft(request):
    """Save CV draft content"""
    try:
        data = json.loads(request.body)
        content = data.get('content')
        
        if not content:
            return JsonResponse({'success': False, 'error': 'No content provided'})
        
        cv = CV.objects.get(user=request.user)
        cv.content = content
        cv.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
