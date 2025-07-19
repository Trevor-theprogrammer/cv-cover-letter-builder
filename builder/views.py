from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CV, CVSection, CoverLetter, UploadedCV, AICoverLetter, CVAnalysis, Template
from .forms import CVForm, CVSectionForm, CoverLetterForm, CustomUserCreationForm, UploadedCVForm, AICoverLetterForm, TemplateForm
from .ai_services import AICoverLetterService, CVAnalyzer
from .file_handlers import CVFileHandler
from .cv_analyzer import CVScannerService

def home(request):
    return render(request, 'builder/home.html')

@login_required
def dashboard(request):
    cvs = CV.objects.filter(user=request.user)
    uploaded_cvs = UploadedCV.objects.filter(user=request.user)
    ai_cover_letters = AICoverLetter.objects.filter(uploaded_cv__user=request.user)[:5]
    return render(request, 'builder/dashboard.html', {
        'cvs': cvs,
        'uploaded_cvs': uploaded_cvs,
        'ai_cover_letters': ai_cover_letters
    })

@login_required
def create_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            messages.success(request, 'CV created successfully!')
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = CVForm()
    return render(request, 'builder/create_cv.html', {'form': form})

@login_required
def cv_detail(request, pk):
    cv = get_object_or_404(CV, pk=pk, user=request.user)
    sections = cv.cvsection_set.all()
    return render(request, 'builder/cv_detail.html', {'cv': cv, 'sections': sections})

@login_required
def add_cv_section(request, cv_pk):
    cv = get_object_or_404(CV, pk=cv_pk, user=request.user)
    
    if request.method == 'POST':
        form = CVSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cv = cv
            section.save()
            messages.success(request, 'Section added successfully!')
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = CVSectionForm()
    
    return render(request, 'builder/add_cv_section.html', {'form': form, 'cv': cv})

@login_required
def edit_cv_section(request, pk):
    section = get_object_or_404(CVSection, pk=pk, cv__user=request.user)
    
    if request.method == 'POST':
        form = CVSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section updated successfully!')
            return redirect('cv_detail', pk=section.cv.pk)
    else:
        form = CVSectionForm(instance=section)
    
    return render(request, 'builder/edit_cv_section.html', {'form': form, 'section': section})

@login_required
def delete_cv_section(request, pk):
    section = get_object_or_404(CVSection, pk=pk, cv__user=request.user)
    cv_pk = section.cv.pk
    section.delete()
    messages.success(request, 'Section deleted successfully!')
    return redirect('cv_detail', pk=cv_pk)

@login_required
def upload_cv(request):
    """Handle CV file upload and processing"""
    if request.method == 'POST':
        form = UploadedCVForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_cv = form.save(commit=False)
            uploaded_cv.user = request.user
            uploaded_cv.original_filename = request.FILES['file'].name
            uploaded_cv.save()
            
            # Extract text from uploaded file
            extracted_text = CVFileHandler.extract_text_from_file(request.FILES['file'])
            uploaded_cv.extracted_text = extracted_text
            uploaded_cv.processed = True
            uploaded_cv.save()
            
            messages.success(request, 'CV uploaded and processed successfully!')
            return redirect('dashboard')
    else:
        form = UploadedCVForm()
    return render(request, 'builder/upload_cv.html', {'form': form})

@login_required
def ai_cover_letter(request):
    """Generate AI-powered cover letters"""
    generated_letter = None
    
    # Get CV ID from URL parameter
    cv_id = request.GET.get('cv')
    initial_cv = None
    if cv_id:
        try:
            initial_cv = UploadedCV.objects.get(id=cv_id, user=request.user)
        except UploadedCV.DoesNotExist:
            initial_cv = None
    
    if request.method == 'POST':
        form = AICoverLetterForm(request.POST, user=request.user)
        if form.is_valid():
            ai_service = AICoverLetterService()
            
            uploaded_cv = form.cleaned_data['uploaded_cv']
            job_title = form.cleaned_data['job_title']
            job_description = form.cleaned_data['job_description']
            tone = form.cleaned_data['tone']
            
            # Generate cover letter using AI
            generated_letter = ai_service.generate_cover_letter(
                uploaded_cv.extracted_text,
                job_title,
                job_description,
                tone
            )
            
            # Save the generated cover letter
            ai_cover_letter = form.save(commit=False)
            ai_cover_letter.generated_letter = generated_letter
            ai_cover_letter.save()
            
            messages.success(request, 'AI cover letter generated successfully!')
    else:
        # Pass initial CV if provided
        form = AICoverLetterForm(user=request.user)
        if initial_cv:
            form.fields['uploaded_cv'].initial = initial_cv
    
    return render(request, 'builder/ai_cover_letter.html', {
        'form': form,
        'generated_letter': generated_letter
    })

@login_required
def cv_analyzer(request):
    """Analyze uploaded CVs"""
    analyses = []
    
    if request.method == 'POST':
        uploaded_cv_id = request.POST.get('uploaded_cv')
        job_description = request.POST.get('job_description', '')
        
        if uploaded_cv_id:
            uploaded_cv = get_object_or_404(UploadedCV, id=uploaded_cv_id, user=request.user)
            scanner = CVScannerService()
            analysis = scanner.scan_cv(uploaded_cv, job_description)
            analyses.append(analysis)
            
            messages.success(request, 'CV analysis completed!')
    
    # Get user's uploaded CVs
    uploaded_cvs = UploadedCV.objects.filter(user=request.user)
    
    return render(request, 'builder/cv_analyzer.html', {
        'uploaded_cvs': uploaded_cvs,
        'analyses': analyses
    })

@login_required
def templates(request):
    """View all templates"""
    templates = Template.objects.all()
    return render(request, 'builder/templates.html', {'templates': templates})

@login_required
def template_detail(request, pk):
    """View template details"""
    template = get_object_or_404(Template, pk=pk)
    return render(request, 'builder/template_detail.html', {'template': template})

@login_required
def create_template(request):
    """Create new template"""
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save()
            messages.success(request, 'Template created successfully!')
            return redirect('templates')
    else:
        form = TemplateForm()
    return render(request, 'builder/create_template.html', {'form': form})

@login_required
def edit_template(request, pk):
    """Edit existing template"""
    template = get_object_or_404(Template, pk=pk)
    
    if request.method == 'POST':
        form = TemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template updated successfully!')
            return redirect('templates')
    else:
        form = TemplateForm(instance=template)
    
    return render(request, 'builder/edit_template.html', {'form': form, 'template': template})

@login_required
def generate_cover_letter(request):
    generated_letter = None
    
    if request.method == 'POST':
        form = CoverLetterForm(request.POST, user=request.user)
        if form.is_valid():
            cv_type = form.cleaned_data['cv_type']
            job_title = form.cleaned_data['job_title']
            job_description = form.cleaned_data['job_description']
            
            if cv_type == 'created':
                cv = form.cleaned_data['cv']
                cv_title = cv.title
                cv_content = "\n".join([section.content for section in cv.cvsection_set.all()])
            else:
                uploaded_cv = form.cleaned_data['uploaded_cv']
                cv_title = uploaded_cv.original_filename
                cv_content = uploaded_cv.extracted_text

            # Enhanced cover letter generation
            generated_letter = (
                f"Dear Hiring Manager,\n\n"
                f"I am writing to express my interest in the {job_title} position. "
                f"My background and experience, as detailed in my {'CV' if cv_type == 'created' else 'uploaded file'} '{cv_title}', "
                f"make me a strong candidate for this role.\n\n"
                f"Key qualifications include:\n"
            )
            
            # Add CV content
            if cv_type == 'created':
                sections = cv.cvsection_set.all()
                for section in sections:
                    generated_letter += f"- {section.content[:100]}...\n"
            else:
                # For uploaded CVs, use extracted text
                lines = cv_content.split('\n')[:5]  # First 5 lines
                for line in lines:
                    if line.strip():
                        generated_letter += f"- {line.strip()[:100]}...\n"
            
            generated_letter += (
                f"\nBased on the job description: {job_description[:200]}...\n\n"
                f"I am confident that my skills and experience align well with your requirements.\n\n"
                f"Thank you for your consideration.\n\n"
                f"Sincerely,\n{request.user.username}"
            )

            # Only save for created CVs since CoverLetter model expects CV instance
            if cv_type == 'created':
                CoverLetter.objects.create(
                    cv=cv,
                    job_title=job_title,
                    job_description=job_description,
                    generated_letter=generated_letter
                )
    else:
        form = CoverLetterForm(user=request.user)

    return render(request, 'builder/generate_cover_letter.html', {
        'form': form, 
        'generated_letter': generated_letter
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def delete_cv(request, pk):
    """Delete a created CV"""
    cv = get_object_or_404(CV, pk=pk, user=request.user)
    if request.method == 'POST':
        cv_title = cv.title
        cv.delete()
        messages.success(request, f'CV "{cv_title}" deleted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def delete_uploaded_cv(request, pk):
    """Delete an uploaded CV file"""
    uploaded_cv = get_object_or_404(UploadedCV, id=pk, user=request.user)
    if request.method == 'POST':
        filename = uploaded_cv.original_filename
        uploaded_cv.file.delete()  # Delete the actual file
        uploaded_cv.delete()
        messages.success(request, f'Uploaded CV "{filename}" deleted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')
