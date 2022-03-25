from datetime import date

from plantio.models import Plantio

from rest_framework import serializers


class PlantioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plantio
        # fields = ('idPlantio', 'cultura', 'talhao', 'dataPlantio', 'estado')
        fields = ('idPlantio', 'talhao', 'dataPlantio', 'estado')
        read_only_fields = ('idPlantio',)

    def validate_dataPlantio(self, dataPlantio):
        if dataPlantio > date.today():
            raise serializers.ValidationError('Data de plantio no futuro.')
        return dataPlantio
