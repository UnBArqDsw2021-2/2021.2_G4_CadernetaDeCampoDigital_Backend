from datetime import date
from distutils.command.upload import upload

from plantio.models import AplicacaoAgrotoxico

from rest_framework import serializers


class AplicacaoAgrotoxicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AplicacaoAgrotoxico
        fields = (
            'plantio', 'agrotoxico', 'dataAplicacao', 'dosagemAplicacao', 'fotoAgrotoxico'
        )
        extra_kwargs = {
            'agrotoxico': {'required': False},
            'fotoAgrotoxico': {'required': False}
        }

    def validate_dataAplicacao(self, dataAplicacao):
        if dataAplicacao > date.today():
            raise serializers.ValidationError('Data de aplicação no futuro.')
        return dataAplicacao

    def validate(self, data):
        if data.get('agrotoxico'):
            query = AplicacaoAgrotoxico.objects.filter(
                plantio=data['plantio'], agrotoxico=data['agrotoxico'], dataAplicacao=data['dataAplicacao'])

            if query.exists():
                raise serializers.ValidationError(
                    f'Esse agrotóxico já foi aplicado nessa plantação na data {data["dataAplicacao"]}.')

        return data
