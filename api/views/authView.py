from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.user import User
from api.serializers.adotanteSerializer import AdotanteReadSerializer
from api.serializers.tutorSerializer import TutorReadSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user: User = self.user

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }

        adotante_data = None
        tutor_data = None

        if hasattr(user, "adotante"):
            adotante_data = AdotanteReadSerializer(user.adotante).data

        if hasattr(user, "tutor"):
            tutor_data = TutorReadSerializer(user.tutor).data

        data["adotante"] = adotante_data
        data["tutor"] = tutor_data

        return data


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description="Login com email e senha. Retorna tokens JWT, dados do usuário e perfil (adotante/tutor).",
        request=CustomTokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(
                description="Login realizado com sucesso (tokens, user, adotante/tutor)."
            ),
            401: OpenApiResponse(description="Credenciais inválidas"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
