from datetime import date

from plantio.models import AplicacaoAgrotoxico

from core.consts.agrotoxicos import AplicacaoEstados

from rest_framework import serializers


class AplicacaoAgrotoxicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AplicacaoAgrotoxico
        fields = (
            'plantio', 'agrotoxico', 'dataAplicacao', 'dosagemAplicacao', 'fotoAgrotoxico', 'estadoAnalise'
        )
        read_only_fields = ('estadoAnalise',)
        extra_kwargs = {
            'agrotoxico': {'required': False},
            'fotoAgrotoxico': {'required': False}
        }

    def create(self, validated_data):
        validated_data["estadoAnalise"] = AplicacaoEstados.SUCESSO

        if validated_data.get("fotoAgrotoxico"):
            validated_data["estadoAnalise"] = AplicacaoEstados.ANALISE

        return super().create(validated_data)

    def validate_dataAplicacao(self, dataAplicacao):
        if dataAplicacao > date.today():
            raise serializers.ValidationError('Data de aplicação no futuro.')
        return dataAplicacao

    def validate(self, data):

        self._validate_agrotoxico_xor_fotoAgrotoxico(data.get('agrotoxico'), data.get('fotoAgrotoxico'))
        self._validate_agrotoxico(data.get('agrotoxico'), data['plantio'], data['dataAplicacao'])

        return data

    def _validate_agrotoxico_xor_fotoAgrotoxico(self, agrotoxico, fotoAgrotoxico):
        if (agrotoxico is not None) ^ (fotoAgrotoxico is not None):
            return

        raise serializers.ValidationError(
            'É necessário enviar ou o agrotóxico ou a foto do agrotóxico.'
        )

    def _validate_agrotoxico(self, agrotoxico, plantio, dataAplicacao):
        if not agrotoxico:
            return

        query = AplicacaoAgrotoxico.objects.filter(
                plantio=plantio, agrotoxico=agrotoxico, dataAplicacao=dataAplicacao)

        if query.exists():
            raise serializers.ValidationError(
                f'Esse agrotóxico já foi aplicado nessa plantação na data {dataAplicacao}.')
