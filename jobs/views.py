from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CategorySerializer
from rest_framework.response import Response
from .models import Category,Job

# Create your views here.
class CategoryListView(APIView):

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)