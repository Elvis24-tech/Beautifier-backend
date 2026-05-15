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

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "buyer")
    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=400
        )

    if email and User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=400
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
    })
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=400
        )
    user = authenticate(username=username, password=password)
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
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", "buyer"),
            "is_admin": user.is_staff,
        }
    })

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
    })