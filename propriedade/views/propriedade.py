from core.consts.usuarios import TECNICO

from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer

from rest_framework.generics import ListCreateAPIView


class PropriedadeAPIView(ListCreateAPIView):
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        if self.request.user.tipo == TECNICO:
            return Propriedade.objects.filter(tecnico=self.request.user.tecnico)
        return Propriedade.objects.filter(produtor=self.request.user.produtor)
