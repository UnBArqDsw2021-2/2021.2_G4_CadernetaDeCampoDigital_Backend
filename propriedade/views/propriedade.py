from core.consts.usuarios import TECNICO

from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer, PropriedadeDetailSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


class PropriedadeAPIView(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return PropriedadeDetailSerializer
        return PropriedadeSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Propriedade.objects.none()

        if self.request.user.tipo == TECNICO:
            return Propriedade.objects.filter(tecnico=self.request.user.tecnico)
        return Propriedade.objects.filter(produtor=self.request.user.produtor)


class PropriedadeRetrieveAPIViewTest(RetrieveAPIView):
    serializer_class = PropriedadeDetailSerializer

    def get_queryset(self):
        return Propriedade.objects.all()
