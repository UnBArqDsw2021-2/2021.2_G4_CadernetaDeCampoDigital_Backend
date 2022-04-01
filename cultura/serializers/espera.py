from cultura.models import Espera

from rest_framework import serializers


class CulturaEsperaAgrotoxicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espera
        fields = ('agrotoxico', 'cultura', 'diasCarencia')
