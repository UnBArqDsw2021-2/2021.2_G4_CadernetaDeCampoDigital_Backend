from core.consts.usuarios import TECNICO

from plantio.models import Plantio
from plantio.serializers.plantio import PlantioListSerializer

from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer, PropriedadeDetailSerializer

from talhao.models import Talhao

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView


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


class PropriedadeRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    def get_queryset(self):
        return Propriedade.objects.all()

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return PropriedadeDetailSerializer
        return PropriedadeSerializer


class PropriedadeHistoricoPlantioAPIView(ListAPIView):
    serializer_class = PlantioListSerializer
    lookup_field = 'idPropriedade'

    def get_queryset(self):
        return Plantio.objects.filter(
            talhao__in=Talhao.objects.filter(**self.kwargs).values_list('idTalhao'))
