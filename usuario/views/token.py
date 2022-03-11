from rest_framework_simplejwt.views import TokenObtainPairView

from usuario.serializers.token import TokenObtainPairSerializer


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
