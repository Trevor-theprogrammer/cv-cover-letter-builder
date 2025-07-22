from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AICoverLetter, UploadedCV, CVAnalysis, Template, CV, CVSection

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UploadedCVForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Software Engineer CV'
        })
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Brief description of this CV...'
        })
    )

    class Meta:
        model = UploadedCV
        fields = ['file', 'title', 'description']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt'
            })
        }

class AICoverLetterForm(forms.ModelForm):
    class Meta:
        model = AICoverLetter
        fields = ['uploaded_cv', 'job_title', 'job_description']
        widgets = {
            'uploaded_cv': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Job Description'})
        }

class CVCreationForm(forms.Form):
    """Form for creating a new CV with all required fields"""
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'John Doe',
            'oninput': 'updatePreview()'
        })
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Software Developer',
            'oninput': 'updatePreview()'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'john@example.com',
            'oninput': 'updatePreview()'
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1-555-123-4567',
            'oninput': 'updatePreview()'
        })
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'San Francisco, CA',
            'oninput': 'updatePreview()'
        })
    )
    linkedin = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'linkedin.com/in/johndoe',
            'oninput': 'updatePreview()'
        })
    )
    summary = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-textarea',
            'placeholder': 'Write a compelling summary highlighting your key achievements, skills, and career objectives...',
            'oninput': 'updatePreview()',
            'rows': 4
        })
    )
    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Python, Django, JavaScript, React, SQL, AWS...',
            'oninput': 'updatePreview()'
        })
    )
    template = forms.ChoiceField(
        choices=[
            ('modern', 'Modern - Clean & Professional'),
            ('classic', 'Classic - Traditional & Elegant'),
            ('minimal', 'Minimal - Simple & Focused'),
            ('creative', 'Creative - Stylish & Unique'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'updatePreview()'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experience_data = []
        self.education_data = []

    def clean(self):
        cleaned_data = super().clean()
        
        # Process experience data
        experience_titles = self.data.getlist('experience_title[]')
        experience_companies = self.data.getlist('experience_company[]')
        experience_durations = self.data.getlist('experience_duration[]')
        experience_locations = self.data.getlist('experience_location[]')
        experience_descriptions = self.data.getlist('experience_description[]')
        
        for i in range(len(experience_titles)):
            if experience_titles[i] or experience_companies[i]:
                self.experience_data.append({
                    'title': experience_titles[i],
                    'company': experience_companies[i],
                    'duration': experience_durations[i] if i < len(experience_durations) else '',
                    'location': experience_locations[i] if i < len(experience_locations) else '',
                    'description': experience_descriptions[i] if i < len(experience_descriptions) else ''
                })
        
        # Process education data
        education_degrees = self.data.getlist('education_degree[]')
        education_schools = self.data.getlist('education_school[]')
        education_years = self.data.getlist('education_year[]')
        education_locations = self.data.getlist('education_location[]')
        
        for i in range(len(education_degrees)):
            if education_degrees[i] or education_schools[i]:
                self.education_data.append({
                    'degree': education_degrees[i],
                    'school': education_schools[i],
                    'year': education_years[i] if i < len(education_years) else '',
                    'location': education_locations[i] if i < len(education_locations) else ''
                })
        
        return cleaned_data
