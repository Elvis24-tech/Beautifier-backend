from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

from .models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# =========================
# REGISTER
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=201)

    return Response(serializer.errors, status=400)


# =========================
# LOGIN (SAFE + FIXED)
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    # validate input
    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=400
        )

    # SAFE lookup (prevents MultipleObjectsReturned crash)
    user_obj = User.objects.filter(email=email).first()

    if not user_obj:
        return Response(
            {"error": "Invalid credentials"},
            status=400
        )

    # authenticate using username (Django default auth system)
    user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=400
        )

    # generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }, status=200)


# =========================
# CURRENT USER
# =========================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })