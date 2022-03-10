from usuario.serializers.usuario import UsuarioSerializer
from core.serializers.fields import DAPField

from usuario.models import Usuario

from produtor.models import Produtor

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ProdutorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    dap = DAPField(validators=[UniqueValidator(queryset=Produtor.objects.all())])
    class Meta:
        model = Produtor
        fields = ('usuario', 'dap')

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_data['tipo'] = Usuario.PRODUTOR
        usuario = UsuarioSerializer().create(usuario_data)
        return Produtor.objects.create(usuario=usuario, **validated_data)
