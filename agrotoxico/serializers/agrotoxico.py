from agrotoxico.models import Agrotoxico

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class AgrotoxicoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(
        max_length=80,
        validators=[UniqueValidator(queryset=Agrotoxico.objects.all())]
    )

    class Meta:
        model = Agrotoxico
        fields = ('idAgrotoxico', 'nome', 'tipo')
        read_only_fields = ('idAgrotoxico',)
