import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.conf import settings
from .enhanced_ai_services_fixed import EnhancedAICoverLetterService
from .models import AICoverLetter, CVAnalysis
from .enhanced_forms import EnhancedCoverLetterForm

logger = logging.getLogger(__name__)

@login_required
def enhanced_ai_cover_letter(request):
    """Enhanced AI cover letter generator view"""
    if request.method == 'POST':
        form = EnhancedCoverLetterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Process form data
                job_title = form.cleaned_data['job_title']
                job_description = form.cleaned_data['job_description']
                tone = form.cleaned_data.get('tone', 'professional')
                template_type = form.cleaned_data.get('template_type', 'standard')
                
                # Get CV text
                cv_text = form.cleaned_data.get('cv_text', '')
                if form.cleaned_data.get('uploaded_cv'):
                    # Process uploaded CV file
                    cv_file = form.cleaned_data['uploaded_cv']
                    cv_text = cv_file.read().decode('utf-8', errors='ignore')[:5000]
                
                # Generate cover letter
                service = EnhancedAICoverLetterService()
                cv_insights = service.extract_cv_insights(cv_text)
                job_match = service.match_cv_to_job(cv_insights, job_title, job_description)
                cover_letter = service.generate_tailored_cover_letter(
                    cv_insights, job_match, job_title, job_description, tone, template_type
                )
                
                # Save to database
                ai_cover_letter = AICoverLetter.objects.create(
                    user=request.user,
                    job_title=job_title,
                    job_description=job_description,
                    generated_letter=cover_letter,
                    cv_analysis=cv_text[:500],
                    tone=tone,
                    template_type=template_type
                )
                
                return render(request, 'builder/enhanced_ai_cover_letter_result.html', {
                    'cover_letter': cover_letter,
                    'cv_insights': cv_insights,
                    'job_match': job_match,
                    'ai_cover_letter': ai_cover_letter
                })
                
            except Exception as e:
                logger.error(f"Cover letter generation failed: {str(e)}")
                return render(request, 'builder/enhanced_ai_cover_letter.html', {
                    'form': form,
                    'error': 'Failed to generate cover letter. Please try again.'
                })
    else:
        form = EnhancedCoverLetterForm()
    
    return render(request, 'builder/enhanced_ai_cover_letter.html', {'form': form})

@login_required
def ajax_generate_cover_letter(request):
    """AJAX endpoint for real-time cover letter generation"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        data = json.loads(request.body)
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        cv_text = data.get('cv_text', '')
        tone = data.get('tone', 'professional')
        
        if not all([job_title, job_description]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        service = EnhancedAICoverLetterService()
        cv_insights = service.extract_cv_insights(cv_text)
        job_match = service.match_cv_to_job(cv_insights, job_title, job_description)
        cover_letter = service.generate_tailored_cover_letter(
            cv_insights, job_match, job_title, job_description, tone
        )
        
        return JsonResponse({
            'success': True,
            'cover_letter': cover_letter,
            'cv_insights': cv_insights,
            'job_match': job_match
        })
        
    except Exception as e:
        logger.error(f"AJAX generation failed: {str(e)}")
        return JsonResponse({'error': 'Generation failed'}, status=500)

@login_required
def edit_generated_letter(request, pk):
    """Edit saved generated cover letter"""
    ai_cover_letter = get_object_or_404(AICoverLetter, pk=pk, user=request.user)
    
    if request.method == 'POST':
        new_letter = request.POST.get('generated_letter', '')
        if new_letter:
            ai_cover_letter.generated_letter = new_letter
            ai_cover_letter.save()
            return redirect('enhanced_ai_cover_letter')
    
    return render(request, 'builder/edit_generated_letter.html', {
        'ai_cover_letter': ai_cover_letter
    })

@login_required
def cv_analysis_detail(request, pk):
    """Detailed CV analysis view"""
    cv_analysis = get_object_or_404(CVAnalysis, pk=pk, user=request.user)
    return render(request, 'builder/cv_analysis_detail.html', {
        'cv_analysis': cv_analysis
    })
