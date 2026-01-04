from django.db import models
from django.contrib.auth.models import AbstractUser
from companies.models import Company
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('RECRUITER', 'Recruiter'),
        ('JOB_SEEKER', 'Job Seeker'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recruiters',null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Recruiter"