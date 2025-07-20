from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AICoverLetter, UploadedCV, CVAnalysis, Template

class CustomUserCreationForm(UserCreationForm):
    """Enhanced user creation form with additional fields"""
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

class EnhancedAICoverLetterForm(forms.ModelForm):
    """Enhanced form for AI cover letter generation"""
    cv_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Paste your CV content here or upload a file below...'
        }),
        required=False,
        label='CV Content'
    )
    
    tone = forms.ChoiceField(
        choices=[
            ('professional', 'Professional'),
            ('friendly', 'Friendly'),
            ('formal', 'Formal'),
            ('creative', 'Creative'),
            ('confident', 'Confident'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='professional'
    )
    
    template_type = forms.ChoiceField(
        choices=[
            ('standard', 'Standard'),
            ('modern', 'Modern'),
            ('executive', 'Executive'),
            ('creative', 'Creative'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='standard'
    )

    class Meta:
        model = AICoverLetter
        fields = ['uploaded_cv', 'job_title', 'job_description', 'tone']
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Senior Software Engineer'
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Paste the job description here...'
            }),
            'uploaded_cv': forms.Select(attrs={'class': 'form-control'})
        }

class UploadedCVForm(forms.ModelForm):
    """Form for uploading CV files"""
    class Meta:
        model = UploadedCV
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt'
            })
        }

class TemplateForm(forms.ModelForm):
    """Form for creating CV templates"""
    class Meta:
        model = Template
        fields = ['name', 'description', 'template_content', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Template name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of this template'
            }),
            'template_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 20,
                'placeholder': 'Template content with placeholders...'
            }),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
