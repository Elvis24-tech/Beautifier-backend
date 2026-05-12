from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()

# ✅ FIX: empty prefix removes /orders/orders/ bug
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]