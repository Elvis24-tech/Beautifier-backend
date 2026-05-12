from django.urls import path
from .views import (
    stk_push_view,
    mpesa_callback,
)

urlpatterns = [
    path("stkpush/", stk_push_view),
    path("callback/", mpesa_callback),
]