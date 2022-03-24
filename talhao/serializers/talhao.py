from rest_framework import serializers

from propriedade.serializers.propriedade import PropriedadeSerializer
from propriedade.models.propriedade import Propriedade

from talhao.models import Talhao


class TalhaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talhao
        fields = ('idPropriedade', 'numero')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Talhao.objects.all(),
                fields=('idPropriedade', 'numero'),
                message='Este número de talhão já existe nessa propriedade.'
            )
        ]
        