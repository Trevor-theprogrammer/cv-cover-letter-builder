from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CV, CoverLetter, CVSection, UploadedCV, AICoverLetter, Template

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['title']

class CoverLetterForm(forms.Form):
    cv_type = forms.ChoiceField(
        choices=[('created', 'Created CV'), ('uploaded', 'Uploaded CV')],
        widget=forms.RadioSelect,
        initial='created'
    )
    cv = forms.ModelChoiceField(
        queryset=CV.objects.none(),
        required=False,
        label="Select Created CV"
    )
    uploaded_cv = forms.ModelChoiceField(
        queryset=UploadedCV.objects.none(),
        required=False,
        label="Select Uploaded CV"
    )
    job_title = forms.CharField(max_length=200)
    job_description = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cv'].queryset = CV.objects.filter(user=user)
            self.fields['uploaded_cv'].queryset = UploadedCV.objects.filter(user=user)
    
    def clean(self):
        cleaned_data = super().clean()
        cv_type = cleaned_data.get('cv_type')
        cv = cleaned_data.get('cv')
        uploaded_cv = cleaned_data.get('uploaded_cv')
        
        if cv_type == 'created' and not cv:
            raise forms.ValidationError("Please select a created CV.")
        if cv_type == 'uploaded' and not uploaded_cv:
            raise forms.ValidationError("Please select an uploaded CV.")
        
        return cleaned_data

class CVSectionForm(forms.ModelForm):
    class Meta:
        model = CVSection
        fields = ['content']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UploadedCVForm(forms.ModelForm):
    class Meta:
        model = UploadedCV
        fields = ['file', 'original_filename']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'original_filename': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CV Title'})
        }

class AICoverLetterForm(forms.ModelForm):
    class Meta:
        model = AICoverLetter
        fields = ['job_description', 'job_title', 'tone']
        widgets = {
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'tone': forms.Select(attrs={'class': 'form-select'})
        }

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'description', 'template_content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'template_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }
