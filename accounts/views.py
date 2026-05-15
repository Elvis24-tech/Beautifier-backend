from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema, OpenApiExample

User = get_user_model()
@extend_schema(
    summary="Register User",
    description="Creates a new buyer/farmer account",
    examples=[
        OpenApiExample(
            "Register Example",
            value={
                "username": "elvis",
                "email": "elvis@gmail.com",
                "password": "123456",
                "role": "buyer"
            },
            request_only=True,
        )
    ]
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "buyer")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if email and User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if hasattr(user, "role"):
        user.role = role
        user.save()

    return Response({
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", "buyer"),
        }
    }, status=status.HTTP_201_CREATED)

@extend_schema(
    summary="Login User",
    description="Returns JWT access and refresh tokens"
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", "buyer"),
            "is_admin": user.is_staff,
        }
    }, status=status.HTTP_200_OK)

@extend_schema(
    summary="Get Current User",
    description="Returns logged-in user profile"
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": getattr(user, "role", "buyer"),
        "is_admin": user.is_staff,
    }, status=status.HTTP_200_OK)