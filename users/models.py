from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_customer = models.BooleanField(default=True)

    @property
    def is_admin_user(self):
        return self.email == "elvis@beautyshop.com"