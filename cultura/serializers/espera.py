from cultura.models import Espera

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class CulturaEsperaAgrotoxicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espera
        fields = ('agrotoxico', 'cultura', 'diasCarencia')
        validators = [
            UniqueTogetherValidator(
                queryset=Espera.objects.all(),
                fields=('agrotoxico', 'cultura'),
                message='Cultura já relacionada com agrotóxico.'
            ),
        ]
