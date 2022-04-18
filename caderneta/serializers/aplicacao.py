from rest_framework import serializers

from plantio.models import AplicacaoAgrotoxico
from cultura.models import Espera

from agrotoxico.serializers.agrotoxico import AgrotoxicoListSerializer


class AplicacaoSerializer(serializers.ModelSerializer):
    agrotoxico = AgrotoxicoListSerializer()
    diasCarencia = serializers.SerializerMethodField()

    class Meta:
        model = AplicacaoAgrotoxico
        fields = (
            'idAplicacao', 'agrotoxico', 'dataAplicacao',
            'fotoAgrotoxico', 'dosagemAplicacao', 'estadoAnalise', 'diasCarencia'
        )

    def get_diasCarencia(self, aplicacao):
        if aplicacao.agrotoxico is None:
            return None

        espera = Espera.objects.filter(cultura=aplicacao.plantio.cultura, agrotoxico=aplicacao.agrotoxico).first()
        return espera.diasCarencia if espera else None
