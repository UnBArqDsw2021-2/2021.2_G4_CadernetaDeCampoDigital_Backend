from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Nenhuma conta encontrada. CPF ou senha incorretos.'
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'idUsuario': str(self.user.idUsuario)})
        data.update({'cpf': self.user.cpf})
        data.update({'nome': self.user.nome})
        data.update({'tipo': self.user.tipo})
        return data
