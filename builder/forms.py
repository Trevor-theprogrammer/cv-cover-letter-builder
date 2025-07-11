from django import forms
from .models import CV, CVSection, CoverLetter

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['title']

class CVSectionForm(forms.ModelForm):
    class Meta:
        model = CVSection
        fields = ['heading', 'content']

class CoverLetterForm(forms.ModelForm):
    class Meta:
        model = CoverLetter
        fields = ['cv', 'job_title', 'job_description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cv'].queryset = CV.objects.filter(user=user)
        else:
            self.fields['cv'].queryset = CV.objects.none()