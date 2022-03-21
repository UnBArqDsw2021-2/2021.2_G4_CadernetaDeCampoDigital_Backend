from core.serializers.fields import CEPField, CPFField

from propriedade.models import Propriedade

from rest_framework import serializers

from produtor.models.produtor import Produtor

from tecnico.models.tecnico import Tecnico


class PropriedadeSerializer(serializers.ModelSerializer):
    produtor = CPFField()
    tecnico = CPFField(required=False)
    cep = CEPField()

    class Meta:
        model = Propriedade
        fields = (
            'idPropriedade', 'cep', 'estado', 'cidade',
            'bairro', 'complemento', 'numeroCasa', 'hectares',
            'logradouro', 'produtor', 'tecnico'
        )
        read_only_fields = ('idPropriedade',)
        extra_kwargs = {
            'complemento': {'required': False},
            'hectares': {'required': False}
        }

    def validate_produtor(self, produtor):
        try:
            produtor = Produtor.objects.get(usuario__cpf=produtor)
            return produtor
        except Produtor.DoesNotExist:
            raise serializers.ValidationError('Produtor não existe.')

    def validate_tecnico(self, tecnico):
        try:
            tecnico = Tecnico.objects.get(usuario__cpf=tecnico)
            return tecnico
        except Tecnico.DoesNotExist:
            raise serializers.ValidationError('Técnico não existe.')
