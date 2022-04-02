from agrotoxico.models import Agrotoxico
from agrotoxico.serializers.tipo_agrotoxico import TipoAgrotoxicoSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class AgrotoxicoCreateSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(
        max_length=80,
        validators=[UniqueValidator(queryset=Agrotoxico.objects.all())]
    )

    class Meta:
        model = Agrotoxico
        fields = ('idAgrotoxico', 'nome', 'tipo')
        read_only_fields = ('idAgrotoxico',)


class AgrotoxicoListSerializer(AgrotoxicoCreateSerializer):
    tipo = TipoAgrotoxicoSerializer()

    class Meta(AgrotoxicoCreateSerializer.Meta):
        read_only_fields = AgrotoxicoCreateSerializer.Meta.fields
