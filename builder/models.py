from django.db import models
from django.contrib.auth.models import User

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class CVSection(models.Model):
    cv = models.ForeignKey(CV, related_name='sections', on_delete=models.CASCADE)
    heading = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"{self.heading} ({self.cv.title})"

class CoverLetter(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    generated_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cover Letter for {self.job_title}"
