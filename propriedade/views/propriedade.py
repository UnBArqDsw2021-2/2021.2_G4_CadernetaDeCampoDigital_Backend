from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer

from rest_framework.generics import CreateAPIView


class PropriedadeAPIView(CreateAPIView):
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        return Propriedade.objects.all()