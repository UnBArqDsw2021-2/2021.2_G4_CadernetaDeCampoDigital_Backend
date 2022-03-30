from datetime import date

from plantio.models import AplicacaoAgrotoxico

from rest_framework import serializers


# TODO: As linhas comentadas fazem referência a implementação da issue 152
class AplicacaoAgrotoxicoSerializer(serializers.ModelSerializer):
    # fotoAgrotoxico = serializers

    class Meta:
        model = AplicacaoAgrotoxico
        fields = (
            # 'idAgrotoxico', 'dataAplicacao', 'fotoAgrotoxico', 'dosagemAplicacao'
            'plantio', 'agrotoxico', 'dataAplicacao', 'dosagemAplicacao'
        )

    def validate_dataAplicacao(self, dataAplicacao):
        if dataAplicacao > date.today():
            raise serializers.ValidationError('Data de aplicação no futuro.')
        return dataAplicacao

    def validate(self, data):
        query = AplicacaoAgrotoxico.objects.filter(
            plantio=data['plantio'], agrotoxico=data['agrotoxico'], dataAplicacao=data['dataAplicacao'])

        if query.exists():
            raise serializers.ValidationError(
                f'Esse agrotóxico já foi aplicado nessa plantação na data {data["dataAplicacao"]}.')

        return data
