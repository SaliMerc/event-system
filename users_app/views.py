from users_app.models import CustomUser as User
from users_app.roles import EventAttendeeRole, EventOrganiserRole
from django.contrib.auth.tokens import default_token_generator
from .serializers import *
from django.conf import settings
from users_app.permissions import HasRolePermission
from rolepermissions.roles import assign_role
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.permissions import AllowAny
from rest_framework import status

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password', 'defaultpassword'))
            user.is_active = True
            if user.role == 'organiser':
                assign_role(user, EventOrganiserRole)
            elif user.role == 'attendee':
                assign_role(user, EventAttendeeRole)
            user.save()

            return Response({
                "result_code": 0,
                "message": "User created successfully.",
                "data": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "result_code": 1,
                "message": serializer.errors,
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    access = refresh.access_token
                    return Response({
                        "result_code": 0,
                        "message": "You have logged in successfully",
                        "data": {
                            "refresh": str(refresh),
                            "access": str(access),
                            'user' : UserSerializer(user, context={'request': request}).data
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "result_code": 1,
                        "message": "Invalid credentials. Check your email or password",
                        "data": {}
                    }, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({
                    "result_code": 1,
                    "message": "User not found.",
                    "data": {}
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "result_code": 1,
                "message": serializer.errors,
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)