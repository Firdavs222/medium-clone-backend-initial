from django.shortcuts import render
from rest_framework import status, permissions, generics, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginSerializer, ValidationErrorSerializer, TokenResponseSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

# Create your views here.

User = get_user_model()

# Swagger uchun kerakli sozlamalar
@extend_schema_view(
    post=extend_schema(
        summary="Sign up a new user",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: ValidationErrorSerializer
        }
    )
)


#SignUp uchun view class:
class SignupView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'user': user_data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@extend_schema_view(
    post=extend_schema(
        summary="Log in a user",
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            400: ValidationErrorSerializer,
        }
    )
)    

# Login qilish uchun class
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Hisob maʼlumotlari yaroqsiz'}, status=status.HTTP_401_UNAUTHORIZED)
# Swagger uchun kerakli sozlamalar
@extend_schema_view(
    get=extend_schema(
        summary="Get user information",
        responses={
            200: UserSerializer,
            400: ValidationErrorSerializer
        }
    ),
    patch=extend_schema(
        summary="Update user information",
        request=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
            400: ValidationErrorSerializer
        }
    )
)


# User malumotlarni olish uchum class
class UsersMe(generics.RetrieveAPIView, generics.UpdateAPIView):
    http_method_names = ['get','patch']
    queryset = User.objects.filter(is_active=True)
    parser_classes = [parsers.MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        return UserSerializer