from users.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    birthdate = serializers.DateField(default=None)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_employee = serializers.BooleanField(default=False)
    password = serializers.CharField(max_length=127, write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_email(self, email_exists):
        if User.objects.filter(email=email_exists).exists():
            raise ValidationError("email already registered.")
        return email_exists

    def validate_username(self, username_exists):
        if User.objects.filter(username=username_exists).exists():
            raise ValidationError("username already taken.")
        return username_exists

    def create(self, validated_data: dict):
        if (validated_data["is_employee"] is False) or (
            validated_data["is_employee"] is None
        ):
            user = User.objects.create_user(**validated_data)
        else:
            validated_data["is_superuser"] = True
            user = User.objects.create_superuser(**validated_data)
        return user

    def update(self, instance: User, validated_data: dict):
        for key, value in validated_data.items():
            if key == "password" and value:
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser

        return token
