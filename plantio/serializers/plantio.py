from datetime import date

from cultura.serializers.cultura import CulturaSerializer

from plantio.models import Plantio

from rest_framework import serializers


class PlantioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plantio
        fields = ('idPlantio', 'cultura', 'talhao', 'dataPlantio', 'estado')
        read_only_fields = ('idPlantio',)

    def validate_dataPlantio(self, dataPlantio):
        if dataPlantio > date.today():
            raise serializers.ValidationError('Data de plantio no futuro.')
        return dataPlantio


class PlantioListSerializer(PlantioSerializer):
    cultura = CulturaSerializer()

    class Meta(PlantioSerializer.Meta):
        fields = PlantioSerializer.Meta.fields
        read_only_fields = fields
