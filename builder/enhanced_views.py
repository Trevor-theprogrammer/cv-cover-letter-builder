from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CV, CVSection, CoverLetter, UploadedCV, AICoverLetter, CVAnalysis, Template
from .enhanced_forms import EnhancedAICoverLetterForm
from .enhanced_ai_services import EnhancedAICoverLetterService
import json

@login_required
def enhanced_ai_cover_letter(request):
    """Enhanced AI cover letter generation with deep CV analysis"""
    generated_letter = None
    cv_insights = None
    job_match = None
    
    if request.method == 'POST':
        form = EnhancedAICoverLetterForm(request.POST, user=request.user)
        if form.is_valid():
            ai_service = EnhancedAICoverLetterService()
            
            uploaded_cv = form.cleaned_data['uploaded_cv']
            job_title = form.cleaned_data['job_title']
            job_description = form.cleaned_data['job_description']
            tone = form.cleaned_data['tone']
            template_type = form.cleaned_data['template_type']
            company_research = form.cleaned_data['company_research']
            
            # Add company research to job description if provided
            if company_research:
                job_description = f"{job_description}\n\nCompany Research: {company_research}"
            
            # Step 1: Extract deep insights from CV
            cv_insights = ai_service.extract_cv_insights(uploaded_cv.extracted_text)
            
            # Step 2: Match CV to job requirements
            job_match = ai_service.match_cv_to_job(cv_insights, job_title, job_description)
            
            # Step 3: Generate tailored cover letter
            generated_letter = ai_service.generate_tailored_cover_letter(
                cv_insights, job_match, job_title, job_description, tone, template_type
            )
            
            # Save the generated cover letter
            ai_cover_letter = AICoverLetter.objects.create(
                uploaded_cv=uploaded_cv,
                job_title=job_title,
                job_description=job_description,
                generated_letter=generated_letter,
                tone=tone
            )
            
            messages.success(request, 'AI cover letter generated successfully with deep CV analysis!')
            
            # Store insights in session for display
            request.session['cv_insights'] = json.dumps(cv_insights, indent=2)
            request.session['job_match'] = json.dumps(job_match, indent=2)
    else:
        # Get CV ID from URL parameter
        cv_id = request.GET.get('cv')
        initial_cv = None
        if cv_id:
            try:
                initial_cv = UploadedCV.objects.get(id=cv_id, user=request.user)
            except UploadedCV.DoesNotExist:
                initial_cv = None
        
        form = EnhancedAICoverLetterForm(user=request.user)
        if initial_cv:
            form.fields['uploaded_cv'].initial = initial_cv
    
    return render(request, 'builder/enhanced_ai_cover_letter.html', {
        'form': form,
        'generated_letter': generated_letter,
        'cv_insights': cv_insights,
        'job_match': job_match,
        'cv_insights_json': request.session.pop('cv_insights', None),
        'job_match_json': request.session.pop('job_match', None)
    })

@login_required
def preview_cover_letter(request):
    """Preview cover letter before saving"""
    if request.method == 'POST':
        letter_content = request.POST.get('letter_content', '')
        return render(request, 'builder/preview_cover_letter.html', {
            'letter_content': letter_content
        })
    return redirect('enhanced_ai_cover_letter')

@login_required
def edit_generated_letter(request, pk):
    """Edit a generated AI cover letter"""
    ai_letter = get_object_or_404(AICoverLetter, pk=pk, uploaded_cv__user=request.user)
    
    if request.method == 'POST':
        edited_content = request.POST.get('edited_letter', '')
        ai_letter.generated_letter = edited_content
        ai_letter.save()
        messages.success(request, 'Cover letter updated successfully!')
        return redirect('dashboard')
    
    return render(request, 'builder/edit_generated_letter.html', {
        'ai_letter': ai_letter
    })

@login_required
def cv_analysis_detail(request, pk):
    """Detailed CV analysis view"""
    uploaded_cv = get_object_or_404(UploadedCV, pk=pk, user=request.user)
    
    # Get or create analysis
    try:
        analysis = CVAnalysis.objects.get(uploaded_cv=uploaded_cv)
    except CVAnalysis.DoesNotExist:
        # Create analysis if it doesn't exist
        ai_service = EnhancedAICoverLetterService()
        cv_insights = ai_service.extract_cv_insights(uploaded_cv.extracted_text)
        
        analysis = CVAnalysis.objects.create(
            uploaded_cv=uploaded_cv,
            overall_score=85,  # This would be calculated
            strengths=cv_insights.get('key_achievements', []),
            improvements=[],
            keywords={'extracted': cv_insights.get('core_skills', [])},
            experience_level='Senior'  # This would be determined
        )
    
    return render(request, 'builder/cv_analysis_detail.html', {
        'uploaded_cv': uploaded_cv,
        'analysis': analysis,
        'cv_insights': json.dumps(analysis.strengths, indent=2)
    })

@login_required
def ajax_generate_cover_letter(request):
    """AJAX endpoint for real-time cover letter generation"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            uploaded_cv_id = data.get('uploaded_cv')
            job_title = data.get('job_title')
            job_description = data.get('job_description')
            tone = data.get('tone', 'professional')
            template_type = data.get('template_type', 'standard')
            
            uploaded_cv = get_object_or_404(UploadedCV, id=uploaded_cv_id, user=request.user)
            
            ai_service = EnhancedAICoverLetterService()
            cv_insights = ai_service.extract_cv_insights(uploaded_cv.extracted_text)
            job_match = ai_service.match_cv_to_job(cv_insights, job_title, job_description)
            generated_letter = ai_service.generate_tailored_cover_letter(
                cv_insights, job_match, job_title, job_description, tone, template_type
            )
            
            return JsonResponse({
                'success': True,
                'letter': generated_letter,
                'insights': cv_insights,
                'match': job_match
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def cover_letter_templates(request):
    """View and manage cover letter templates"""
    templates = Template.objects.all()
    return render(request, 'builder/cover_letter_templates.html', {
        'templates': templates
    })

@login_required
def use_template(request, template_id):
    """Use a template for cover letter generation"""
    template = get_object_or_404(Template, id=template_id)
    
    if request.method == 'POST':
        form = EnhancedAICoverLetterForm(request.POST, user=request.user)
        if form.is_valid():
            # Generate letter using template structure
            ai_service = EnhancedAICoverLetterService()
            uploaded_cv = form.cleaned_data['uploaded_cv']
            job_title = form.cleaned_data['job_title']
            job_description = form.cleaned_data['job_description']
            tone = form.cleaned_data['tone']
            
            cv_insights = ai_service.extract_cv_insights(uploaded_cv.extracted_text)
            job_match = ai_service.match_cv_to_job(cv_insights, job_title, job_description)
            
            # Apply template structure
            generated_letter = ai_service.generate_tailored_cover_letter(
                cv_insights, job_match, job_title, job_description, tone, 'standard'
            )
            
            return render(request, 'builder/enhanced_ai_cover_letter.html', {
                'form': form,
                'generated_letter': generated_letter,
                'template_used': template
            })
    
    else:
        form = EnhancedAICoverLetterForm(user=request.user)
    
    return render(request, 'builder/use_template.html', {
        'form': form,
        'template': template
    })
