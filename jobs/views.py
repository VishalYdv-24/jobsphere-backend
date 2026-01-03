from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from .serializers import CategorySerializer
from rest_framework.response import Response
from .models import Category,Job

# Create your views here.
class CategoryListCreateView(APIView):
    """
    GET -> Public
    POST -> Admin only
    """

    permission_classes = [permissions.AllowAny]

    # Category list can be view by any user
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    # only admin (staff) can add, update or delete categories 
    def post(self,request):
        # if not request.user.is_staff:
        #     return Response(
        #         {"error" : "Only admin can access this."}
        #     )
        # serializer = CategorySerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(
        #         serializer.data, status=status.HTTP_201_CREATED
        #     )
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message" : "Category Created successfully",
                    "data" : serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """
    PUT -> Admin only
    DELETE -> Admin only
    """


    # retrive category 
    def get_object(self,pk):
        try :
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None
        
    # update retrive category
    def put(self,request,pk):
        # if not request.user.is_staff:
        #     return Response(
        #         {"error" : "Only Admin can access this."}
        #     )
        
        category = self.get_object(pk)
        if not category:
            return Response(
                {"error" : "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message' : 'Category updated successfully',
                    'data' : serializer.data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # delete retrive category
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {'error' : "Only admin can access this"}
            )
        
        category = self.get_object(pk)
        if not category:
            return Response(
                {"error" : "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        category.delete()
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_200_OK
        )