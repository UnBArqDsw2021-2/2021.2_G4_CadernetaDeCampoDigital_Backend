from rest_framework import serializers

from plantio.serializers.plantio import PlantioListSerializer

from talhao.models import Talhao


class TalhaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talhao
        fields = ('idPropriedade', 'numero')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Talhao.objects.all(),
                fields=('idPropriedade', 'numero'),
                message='Este número de talhão já existe nessa propriedade.'
            )
        ]


class TalhaoListSerializer(serializers.ModelSerializer):
    plantio = serializers.SerializerMethodField()

    class Meta:
        model = Talhao
        fields = ('idPropriedade', 'numero', 'plantio')
        read_only_fields = fields

    def get_plantio(self, talhao):
        if bool(self.context):
            plantios = talhao.plantio_set.filter(
                estado__in=self.context
            )
        else:
            plantios = talhao.plantio_set.all()

        return PlantioListSerializer(plantios, many=True).data
