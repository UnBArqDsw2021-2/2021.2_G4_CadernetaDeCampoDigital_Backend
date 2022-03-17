from core.serializers.fields import CPFField

from rest_framework.validators import UniqueValidator

from usuario.models import Usuario

from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):
    cpf = CPFField(validators=[UniqueValidator(queryset=Usuario.objects.all())])
    senha = serializers.CharField(min_length=8, max_length=100, write_only=True)

    class Meta:
        model = Usuario
        fields = ('cpf', 'dataNascimento', 'telefone', 'nome', 'tipo', 'senha')
        read_only_fields = ('tipo',)

    def create(self, validated_data):
        raise NotImplemented('Método create não implementado pela classe pai.')
