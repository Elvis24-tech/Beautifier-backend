from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_admin",
        ]

    def create(self, validated_data):
        is_admin = validated_data.pop("is_admin", False)

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        if is_admin:
            user.is_staff = True
            user.save()

        return user