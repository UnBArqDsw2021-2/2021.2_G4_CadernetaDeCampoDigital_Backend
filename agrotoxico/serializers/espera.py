from attr import field
from agrotoxico.models import Espera

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class AgrotoxicoEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espera
        fields = ('agrotoxico', 'cultura', 'diasCarencia')
