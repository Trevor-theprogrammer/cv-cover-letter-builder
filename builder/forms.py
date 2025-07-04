from django import forms
from .models import CV, CVSection

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['title']

class CVSectionForm(forms.ModelForm):
    class Meta:
        model = CVSection
        fields = ['heading', 'content']

class CoverLetterForm(forms.Form):
    cv = forms.ModelChoiceField(queryset=CV.objects.none(), label="Select CV")
    job_title = forms.CharField(max_length=100, label="Job Title")
    job_description = forms.CharField(widget=forms.Textarea, label="Job Description")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cv'].queryset = CV.objects.filter(user=user)