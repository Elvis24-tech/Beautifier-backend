from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data

    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    role = data.get("role", "buyer")  

    if not email or not password:
        return Response(
            {"error": "Email and password required"},
            status=400
        )
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=username if username else email,
        email=email,
        password=password,
    )
    if hasattr(user, "role"):
        user.role = role
        user.save()

    return Response({
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": getattr(user, "role", "buyer"),
        }
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password required"},
            status=400
        )

    user = authenticate(username=email, password=password)

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=400
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),

        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": getattr(user, "role", "buyer"),  # 👈 IMPORTANT
            "is_admin": user.is_staff,
        }
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    return Response({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": getattr(user, "role", "buyer"),
        "is_admin": user.is_staff,
    })