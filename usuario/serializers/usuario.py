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
        raise NotImplementedError('Método create não implementado pela classe pai.')

    def update(self, instance, validated_data):
        # NOTE: Esse if é responsável por realizar a atualização
        # das chaves da model de Usuario
        if validated_data.get('usuario'):
            usuario = validated_data.pop('usuario')
            if usuario.get('senha'):
                password = usuario.pop('senha')
                instance.usuario.set_password(password)

            for key, value in usuario.items():
                setattr(instance.usuario, key, value)

            instance.usuario.save()

        # NOTE: Esse loop por sua vez atualza as chaves da entidade específica
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
