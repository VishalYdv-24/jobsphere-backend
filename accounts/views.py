from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer,LoginSerializer, UserListSerializer, RecruiterProfileListSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import RecruiterProfile
from .models import User
# Create your views here.

class SignupView(APIView):

    def post(self,request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message" : "User registered Successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            
            # validated_data already contains tokens + user
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ApproveRecruiterView(APIView):
    """
    PATCH -> Admin can approve or disapprove recruiter
    """
    permission_classes =[IsAdminUser]

    def patch(self,request,pk):
        try :
            recruiter_profile = RecruiterProfile.objects.get(pk=pk)
        except RecruiterProfile.DoesNotExist:
            return Response(
                {'error':"Recruiter not found"},
                status=status.HTTP_404_NOT_FOUND
            )
         # Validate input
        if 'is_approved' not in request.data:
            return Response(
                {"error" : "is_approved field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_approved = request.data['is_approved']

        if not isinstance(is_approved, bool):
            return Response(
                {'error':"is_approved must be true or false"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        recruiter_profile.is_approved = is_approved
        recruiter_profile.save()

        message = ("Recruiter approved successfully" if is_approved else "Recruiter disapproved successfully")

        return Response(
            {
                "message" : message,
                "recruiter_id" : recruiter_profile.id,
                "is_approved" : recruiter_profile.is_approved
            },
            status=status.HTTP_200_OK
        )

class UserListView(APIView):
    """
    GET -> Admin only
    List all users
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RecruiterUserListView(APIView):
    """
    GET -> Admin only
    List users with role = Recruiter
    """

    permission_classes = [IsAdminUser]

    def get(self,request):
        recruiters = User.objects.filter(role='RECRUITER')
        serializer = UserListSerializer(recruiters, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RecruiterProfileListView(APIView):
    """
    GET -> admin only
    List recruiter profiles
    """
    permission_classes = [IsAdminUser]

    def get(self,request):
        recruiters = RecruiterProfile.objects.select_related('user','company')
        serializer = RecruiterProfileListSerializer(recruiters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)