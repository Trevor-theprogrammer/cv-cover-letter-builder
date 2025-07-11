from django.shortcuts import render, redirect
from .models import CV, CVSection, CoverLetter
from .forms import CVForm, CoverLetterForm
import openai  # Only if you plan to use OpenAI
from django.contrib.auth.decorators import login_required
import os  # Added for environment variable access

def home(request):
    return render(request, 'builder/home.html')

@login_required
def dashboard(request):
    cvs = CV.objects.filter(user=request.user)
    return render(request, 'builder/dashboard.html', {'cvs': cvs})

@login_required
def create_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            return redirect('dashboard')
    else:
        form = CVForm()
    return render(request, 'builder/create_cv.html', {'form': form})

@login_required
def generate_cover_letter(request):
    generated_letter = None
    if request.method == 'POST':
        form = CoverLetterForm(request.POST, user=request.user)
        if form.is_valid():
            cv = form.cleaned_data['cv']
            job_title = form.cleaned_data['job_title']
            job_description = form.cleaned_data['job_description']

            openai.api_key = os.getenv('OPENAI_API_KEY')
            prompt = f"Write a cover letter for a {job_title} role. CV title: {cv.title}. Job description: {job_description}"

            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=300
                )
                generated_letter = response.choices[0].text.strip()
                # Save to database
                CoverLetter.objects.create(
                    cv=cv,
                    job_title=job_title,
                    job_description=job_description,
                    generated_letter=generated_letter
                )
            except Exception as e:
                generated_letter = f"Error generating cover letter: {e}"

    else:
        form = CoverLetterForm(user=request.user)
    return render(request, 'builder/generate_cover_letter.html', {'form': form, 'generated_letter': generated_letter})
