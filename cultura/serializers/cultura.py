from agrotoxico.serializers.agrotoxico import AgrotoxicoListSerializer

from cultura.models import Cultura

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CulturaSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(
        max_length=80,
        validators=[UniqueValidator(queryset=Cultura.objects.all())]
    )
    agrotoxicos = AgrotoxicoListSerializer(read_only=True, many=True)
    foto = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = Cultura
        fields = ('idCultura', 'nome', 'agrotoxicos', 'foto')
        read_only_fields = ('idCultura', 'agrotoxicos')
