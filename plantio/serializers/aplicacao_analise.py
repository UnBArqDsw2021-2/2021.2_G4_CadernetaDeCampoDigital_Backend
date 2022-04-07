from plantio.models import AplicacaoAgrotoxico

from plantio.serializers.plantio import PlantioSerializer
from produtor.serializers.produtor import ProdutorSerializer

from rest_framework import serializers


class AplicacaoAgrotoxicoAnaliseSerializer(serializers.ModelSerializer):
    plantio = PlantioSerializer()
    produtor = ProdutorSerializer(source='plantio.talhao.idPropriedade.produtor')

    class Meta:
        model = AplicacaoAgrotoxico
        fields = (
            'plantio', 'agrotoxico', 'dataAplicacao', 'dosagemAplicacao', 'fotoAgrotoxico',
            'estadoAnalise', 'produtor'
        )
