from core.consts.usuarios import TECNICO

from rest_framework.validators import UniqueValidator

from tecnico.models import Tecnico

from usuario.serializers.usuario import UsuarioSerializer
from usuario.models.usuario import Usuario

from core.serializers.fields import CREAField


class TecnicoSerializer(UsuarioSerializer):
    usuario = UsuarioSerializer()
    crea = CREAField(validators=[UniqueValidator(queryset=Tecnico.objects.all(), message='Técnico já cadastrado.')])

    class Meta:
        model = Tecnico
        fields = ('usuario', 'crea', 'formacao', 'email')

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        password = usuario_data.pop('senha')
        usuario = Usuario.objects.create_user(
            usuario_data['cpf'],
            password=password,
            tipo=TECNICO,
            **usuario_data

        )

        return Tecnico.objects.create(
            usuario=usuario, emailVerificado=True,
            **validated_data
        )
