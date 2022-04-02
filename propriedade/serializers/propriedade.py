from core.serializers.fields import CEPField, CPFField
from core.consts.plantios import PLANTIO_CHOICES

from propriedade.models import Propriedade

from rest_framework import serializers

from produtor.models.produtor import Produtor
from produtor.serializers.produtor import ProdutorSerializer

from tecnico.models.tecnico import Tecnico
from tecnico.serializers.tecnico import TecnicoSerializer

from talhao.serializers.talhao import TalhaoListSerializer


class PropriedadeSerializer(serializers.ModelSerializer):
    produtor = CPFField()
    tecnico = CPFField(required=False)
    cep = CEPField()

    class Meta:
        model = Propriedade
        fields = (
            'idPropriedade', 'cep', 'estado', 'cidade',
            'bairro', 'complemento', 'numeroCasa', 'hectares',
            'logradouro', 'produtor', 'tecnico'
        )
        read_only_fields = ('idPropriedade',)
        extra_kwargs = {
            'complemento': {'required': False},
            'hectares': {'required': False}
        }

    def validate_produtor(self, produtor):
        try:
            produtor = Produtor.objects.get(usuario__cpf=produtor)
            return produtor
        except Produtor.DoesNotExist:
            raise serializers.ValidationError('Produtor não existe.')

    def validate_tecnico(self, tecnico):
        try:
            tecnico = Tecnico.objects.get(usuario__cpf=tecnico)
            return tecnico
        except Tecnico.DoesNotExist:
            raise serializers.ValidationError('Técnico não existe.')


class PropriedadeDetailSerializer(PropriedadeSerializer):
    talhao = serializers.SerializerMethodField()
    produtor = ProdutorSerializer()
    tecnico = TecnicoSerializer()

    class Meta(PropriedadeSerializer.Meta):
        fields = PropriedadeSerializer.Meta.fields + ('talhao',)
        read_only_fields = fields

    def get_talhao(self, propriedade):
        return TalhaoListSerializer(
            propriedade.talhao_set,
            context=[PLANTIO_CHOICES[0][0], PLANTIO_CHOICES[1][0], PLANTIO_CHOICES[2][0]],
            many=True
        ).data
