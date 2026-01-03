from django.db import models
from accounts.models import User
from companies.models import Company


# Create your models here.

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# JOB model
class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('REMOTE', 'Remote'),
    )

    EXPERIENCE_CHOICES = (
        ('FRESHER', 'Fresher'),
        ('INTERMEDIATE', 'Intermediate'),
        ('EXPERT','Expert'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    job_type = models.CharField(max_length=20,choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20,choices=EXPERIENCE_CHOICES)
    salary_min = models.IntegerField(null=True,blank=True)
    salary_max = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title