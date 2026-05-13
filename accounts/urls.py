from django.urls import path
from .views import register_view, login_view, me_view

urlpatterns = [
    path("register/", register_view),
    path("login/", login_view),
    path("me/", me_view),
]