from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class CVSection(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='sections')
    heading = models.CharField(max_length=100)
    content = models.TextField()

class CoverLetter(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    letter_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
