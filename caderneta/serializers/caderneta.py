from rest_framework import serializers

from plantio.models import Plantio

from cultura.serializers.cultura import CulturaSerializer
from caderneta.serializers.aplicacao import AplicacaoSerializer
from caderneta.serializers.talhao import TalhaoSerializer


class CadernetaSerializer(serializers.ModelSerializer):
    cultura = CulturaSerializer(fields=('idCultura', 'nome', 'foto'))
    talhao = TalhaoSerializer()
    aplicacoes = AplicacaoSerializer(many=True, source='aplicacaoagrotoxico_set')

    class Meta:
        model = Plantio
        fields = (
            'idPlantio', 'dataPlantio', 'estado', 'cultura', 'talhao',
            'talhao', 'aplicacoes'
        )
