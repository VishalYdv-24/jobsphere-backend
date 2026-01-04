from rest_framework import serializers
from .models import Category, Job

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','icon','created_at')

class JobListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_location = serializers.CharField(source='company.location', read_only=True)

    class Meta:
        model = Job
        fields = (
            'title',
            'description',
            'category',
            'job_type',
            'experience_level',
            'salary_min',
            'salary_max',
            'location',
            'latitude',
            'longitude',
            'company',
        )


class JobDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    company = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'description',
            'job_type',
            'experience_level',
            'salary_min',
            'salary_max',
            'location',
            'latitude',
            'longitude',
            'created_at',
            'category_name',
            'company',
        )

    def get_company(self,obj):
        return {
            'id': obj.company.id,
            "name": obj.company.name,
            "description": obj.company.description,
            "loaction": obj.company.location,
            "latitude": obj.company.latitude,
            "longitude": obj.company.longitude,
            "website": obj.company.website,
            "logo": obj.company.logo,
        }

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'title',
            'description',
            'category',
            'job_type',
            'experience_level',
            'salary_min',
            'salary_max',
            'location',
            'latitude',
            'longitude',
        )

class JobUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'title',
            'description',
            'category',
            'job_type',
            'experience_level',
            'salary_min',
            'salary_max',
            'location',
            'latitude',
            'longitude',
        )   