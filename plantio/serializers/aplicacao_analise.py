from plantio.models import AplicacaoAgrotoxico

from plantio.serializers.plantio import PlantioSerializer
from produtor.serializers.produtor import ProdutorSerializer

from rest_framework import serializers


class AplicacaoAgrotoxicoAnaliseSerializer(serializers.ModelSerializer):
    plantio = PlantioSerializer(read_only=True)
    produtor = ProdutorSerializer(source='propriedade.produtor', read_only=True)

    class Meta:
        model = AplicacaoAgrotoxico
        fields = (
            'idAplicacao', 'plantio', 'agrotoxico', 'dataAplicacao',
            'dosagemAplicacao', 'fotoAgrotoxico', 'estadoAnalise', 'produtor'
        )
        read_only_fields = ('idAplicacao',)
