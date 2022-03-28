from agrotoxico.models import TipoAgrotoxico

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class TipoAgrotoxicoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(
        max_length=80,
        validators=[UniqueValidator(queryset=TipoAgrotoxico.objects.all())]
    )

    class Meta:
        model = TipoAgrotoxico
        fields = ('idTipoAgrotoxico', 'nome')
        read_only_fields = ('idTipoAgrotoxico',)
