from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer



class LogoutAPIView(APIView):
    pass


class UserRegistration(generics.CreateAPIView):
    """API view for user registration."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # TODO: Implement permission classes if user registration is restricted (e.g., AllowAny)
    # permission_classes = [permissions.AllowAny]  # Example permission class

    # TODO: Add throttle classes if you want to limit the number of registrations per IP
    # throttle_classes = [UserThrottle]  # Example throttle class

    # TODO: Consider adding custom logging for successful and failed registration attempts
    # def perform_create(self, serializer):
    #     # Custom logic before saving the user can go here
    #     user = serializer.save()
    #     # Example: Logging the registration
    #     logger.info(f'New user registered: {user.username}')