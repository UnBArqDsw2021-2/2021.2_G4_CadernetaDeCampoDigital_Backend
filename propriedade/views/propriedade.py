from core.consts.usuarios import TECNICO

from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


class PropriedadeAPIView(ListCreateAPIView):
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Propriedade.objects.none()

        if self.request.user.tipo == TECNICO:
            return Propriedade.objects.filter(tecnico=self.request.user.tecnico)
        return Propriedade.objects.filter(produtor=self.request.user.produtor)


class PropriedadeRetrieveAPIViewTest(RetrieveAPIView):
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        return Propriedade.objects.all()
