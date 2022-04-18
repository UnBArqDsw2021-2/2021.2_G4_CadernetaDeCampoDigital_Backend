from rest_framework import serializers

from propriedade.serializers.propriedade import PropriedadeDetailSerializer
from talhao.models import Talhao


class TalhaoSerializer(serializers.ModelSerializer):
    propriedade = PropriedadeDetailSerializer(fields=(
            'idPropriedade', 'cep', 'estado', 'cidade',
            'bairro', 'complemento', 'numeroCasa', 'hectares',
            'logradouro', 'produtor', 'tecnico'
        ), source='idPropriedade')

    class Meta:
        model = Talhao
        fields = ('idTalhao', 'numero', 'propriedade')
