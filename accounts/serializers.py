from rest_framework import serializers
from .models import User, RecruiterProfile
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email','password','first_name','last_name','role',)

    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            role=validated_data['role'],
        )
        # Create recruiter profile automatically
        if user.role == 'RECRUITER':
            RecruiterProfile.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        # Find user by email
        try :
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        
        # Authenticate using username (Django needs username, not email)
        user = authenticate(username=user.username, password=data['password'])

        if not user:
            # password incorrect
            raise serializers.ValidationError("Invalid email or password")
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return response data
        return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                }
            }
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'is_active',
        )

class RecruiterProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    email = serializers.EmailField(source='user.email',read_only=True)
    user_id = serializers.IntegerField(source='user.id',read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = (
            'id',
            'user_id',
            'username',
            'email',
            'is_approved',
            'company',
        )