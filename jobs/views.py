from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from .serializers import CategorySerializer,JobListSerializer,JobDetailSerializer,JobCreateSerializer,JobUpdateSerializer
from rest_framework.response import Response
from .models import Category,Job
from rest_framework.permissions import IsAdminUser,IsAuthenticated

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
        # if not request.user.is_staff:
        #     return Response(
        #         {'error' : "Only admin can access this"}
        #     )
        
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
    

class JobListView(APIView):
    """
    GET -> Public
    """

    def get(self,request):
        jobs = Job.objects.select_related('category', 'company')
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JobDetailView(APIView):
    """
    GET -> Public
    """

    def get(self,request,pk):
        try:
            job = Job.objects.select_related('category','company').get(pk=pk)
        except Job.DoesNotExist:
            return Response(
                    {"error" : "job not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = JobDetailSerializer(job)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class JobCreateView(APIView):
    """
    POST -> Approved Recruiter only
    """
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user

        # Role check
        if user.role != "RECRUITER":
            return Response(
                {"error" : "Only Recruiters can create jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # approval check
        if not user.recruiter_profile.is_approved:
            return Response(
                {'error' : "Recruiter not approved"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = JobCreateSerializer(data=request.data)

        if serializer.is_valid():
            job = serializer.save(
                recruiter=user,
                company=user.recruiter_profile.company
            )

            return Response(
                {
                    "message" : "Job created successfully",
                    "job_id" : job.id
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobUpdateDeleteView(APIView):
    """
    PATCH  -> Recruiter can update ONLY own job
    DELETE -> Recruiter can delete ONLY own job
              Admin can delete ANY job
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Job.objects.get(pk)
        except Job.DoesNotExist:
            return None
        
    def patch(self, request,pk):
        user = request.user
        job = self.get_object(pk)

        if not job:
            return Response(
                {"error" : "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Admin cannot update jobs
        if user.role == "ADMIN":
            return Response(
                {"error" : "Admin cannot update Jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # only recruiter
        if not user.recruiter_profile.is_approved:
            return Response(
                {"error" : "Recruiter not approved"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Ownership check
        if job.recruiter != user:
            return Response(
                {"error" : "You can update only your own jobs"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        serializer = JobUpdateSerializer(
            job, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message" : "Job updated successfully",
                    "data" : serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request):
        user = request.user
        job = self.get_object(pk)

        if not job:
            return Response(
                {"error" : 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Admin can delete ANY job
        if user.roel == "ADMIN":
            job.delete()
            return Response(
                {"message" : "Job deleted by Admin"},
                status=status.HTTP_200_OK
            )
        
        # Recruiter rules
        if user.role != "RECRUITER":
            return Response(
                {"error":"Only recruiters can delete jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not user.recruiter_profile.is_approved:
            return Response(
                {"error" : "Recruiter not approved"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if job.recruiter != user:
            return Response(
                {"error" : "You can delet only your own jobs"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        job.delete()
        return Response(
            {"message" : "Job deleted successfully"},
            status=status.HTTP_200_OK
        )