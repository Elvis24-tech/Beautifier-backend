from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(request):
    return JsonResponse({
        "message": "BeautyShop API is running 🚀",
        "status": "success",
        "endpoints": {
            "token": "/api/token/",
            "refresh": "/api/token/refresh/",
            "me": "/api/auth/me/",
            "products": "/api/products/",
            "orders": "/api/orders/"
        }
    })

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/", include("accounts.urls")),
    path("api/products/", include("products.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/mpesa/", include("payments.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)