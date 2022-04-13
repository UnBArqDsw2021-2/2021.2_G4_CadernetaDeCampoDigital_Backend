from rest_framework import serializers

from plantio.serializers.plantio import PlantioListSerializer

from talhao.models import Talhao


class TalhaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talhao
        fields = ('idTalhao', 'idPropriedade', 'numero')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Talhao.objects.all(),
                fields=('idPropriedade', 'numero'),
                message='Este número de talhão já existe nessa propriedade.'
            )
        ]


class TalhaoDetailSerializer(serializers.ModelSerializer):
    plantio = serializers.SerializerMethodField()

    class Meta:
        model = Talhao
        fields = ('idTalhao', 'idPropriedade', 'numero', 'plantio')
        read_only_fields = fields

    def get_plantio(self, talhao):
        if self.context.get('plantio_estado_filtro'):
            [estados] = [*self.context.values()]
            plantios = talhao.plantio_set.filter(
                estado__in=estados
            )
        else:
            plantios = talhao.plantio_set.all()

        return PlantioListSerializer(plantios, many=True).data
