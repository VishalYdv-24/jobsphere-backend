from django.db import models
from django.contrib.auth.models import AbstractUser
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