from datetime import date

from cultura.serializers.cultura import CulturaSerializer

from plantio.models import Plantio

from rest_framework import serializers

from talhao.models import Talhao


class PlantioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plantio
        fields = ('idPlantio', 'cultura', 'talhao', 'dataPlantio', 'estado')
        read_only_fields = ('idPlantio',)

    def validate_dataPlantio(self, dataPlantio):
        if dataPlantio > date.today():
            raise serializers.ValidationError('Data de plantio no futuro.')
        return dataPlantio

    def update(self, instance, validated_data):
        if(validated_data.get('talhao')):
            talhoes_validos = Talhao.objects.filter(idPropriedade=instance.talhao.idPropriedade)
            if(validated_data.get('talhao') not in talhoes_validos):
                raise serializers.ValidationError({'error': 'Esse talhão não pertence a propriedade onde está localizado esse plantio.'})

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PlantioListSerializer(PlantioSerializer):
    cultura = CulturaSerializer()

    class Meta(PlantioSerializer.Meta):
        fields = PlantioSerializer.Meta.fields
        read_only_fields = fields
