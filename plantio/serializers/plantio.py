from agrotoxico.models import Agrotoxico

from core.consts.agrotoxicos import ESTADOS_CHOICES

from datetime import date

from decimal import Decimal

from plantio.models import Plantio, AssociacaoPlantioAgrotoxico

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


# TODO: As linhas comentadas fazem referência a implementação da issue 152
class PlantioAssociacaoSerializer(serializers.ModelSerializer):
    idAgrotoxico = serializers.UUIDField(format='hex_verbose')
    dataAplicacao = serializers.DateField(required=False, default=date.today())
    # fotoAgrotoxico = serializers
    dosagemAplicacao = serializers.DecimalField(
        max_digits=3, decimal_places=2, min_value=Decimal('0.01'))
    estadoAnalise = serializers.ChoiceField(choices=ESTADOS_CHOICES)
    
    class Meta:
        model = Plantio
        fields = (
            # 'idAgrotoxico', 'dataAplicacao', 'fotoAgrotoxico',
            'idAgrotoxico', 'dataAplicacao',
            'dosagemAplicacao', 'estadoAnalise'
        )

    def validate_idAgrotoxico(self, idAgrotoxico):
        try:
            return Agrotoxico.objects.get(idAgrotoxico=idAgrotoxico)
        except Agrotoxico.DoesNotExist:
            raise serializers.ValidationError(f'Não exite agrotóxico registrado com o id {idAgrotoxico}.')

    def validate_dataAplicacao(self, dataAplicacao):
        if dataAplicacao > date.today():
            raise serializers.ValidationError('Data de aplicação no futuro.')
        return dataAplicacao

    def validate(self, data):
        query = AssociacaoPlantioAgrotoxico.objects.filter(
            plantio=self.instance, agrotoxico=data['idAgrotoxico'], dataAplicacao=data['dataAplicacao'])

        if query.exists():
            raise serializers.ValidationError(
                'Esse agrotóxico já foi aplicado nessa plantação na data {data["dataAplicacao"]}.')

        return data

    def save(self):
        agrotoxico = self.validated_data.pop('idAgrotoxico')
        self.instance.agrotoxico.add(agrotoxico, through_defaults=self.validated_data)
        return self.instance
