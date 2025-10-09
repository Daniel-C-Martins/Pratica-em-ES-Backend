# accounts/auth_serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Diz ao SimpleJWT que o “username_field” é email
    username_field = "email"
