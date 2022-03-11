from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from tecnico.models import Tecnico

from usuario.serializers.usuario import UsuarioSerializer
from usuario.models.usuario import Usuario

from core.serializers.fields import CREAField

class TecnicoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    crea = CREAField(validators=[UniqueValidator(queryset=Tecnico.objects.all(), message='Técnico já cadastrado.')])

    class Meta:
        model = Tecnico
        fields = ('usuario', 'crea', 'formacao', 'email')

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_data['tipo'] = Usuario.TECNICO
        usuario = UsuarioSerializer().create(usuario_data)
        return Tecnico.objects.create(usuario=usuario, emailVerificado=True, **validated_data)
