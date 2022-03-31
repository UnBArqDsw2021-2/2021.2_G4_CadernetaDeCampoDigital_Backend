from agrotoxico.models import Espera

from rest_framework import serializers


class EsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espera
        fields = ('agrotoxico', 'cultura', 'diasCarencia')
        read_only_fields = ('agrotoxico',)
