from core.serializers.fields import CPFField

from phonenumber_field.serializerfields import PhoneNumberField

from usuario.models import Usuario

from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):
    cpf = CPFField()
    dataNascimento = serializers.DateField()
    telefone = PhoneNumberField
    nome = serializers.CharField(max_length=80)
    tipo = serializers.ChoiceField(choices=Usuario.TIPO_ESCOLHAS, read_only=True)
    senha = serializers.CharField(min_length=8, max_length=100, write_only=True)

    class Meta:
        model = Usuario
        fields = ('cpf', 'dataNascimento', 'telefone', 'nome', 'tipo', 'senha')

    def create(self, validated_data):
        username = validated_data['cpf']
        password = validated_data.pop('senha')
        return Usuario.objects.create_user(username, password=password, **validated_data)
