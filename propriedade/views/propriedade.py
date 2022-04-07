from core.consts.usuarios import TECNICO

from plantio.models import Plantio
from plantio.serializers.plantio import PlantioListSerializer

from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer, PropriedadeDetailSerializer

from talhao.models import Talhao

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status


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


class PropriedadeRetrieveAPIView(RetrieveAPIView):
    serializer_class = PropriedadeDetailSerializer

    def get_queryset(self):
        return Propriedade.objects.all()


class PropriedadeHistoricoPlantioAPIView(ListAPIView):
    serializer_class = PlantioListSerializer
    lookup_field = 'idPropriedade'

    def get_queryset(self):
        return Plantio.objects.filter(
            talhao__in=Talhao.objects.filter(**self.kwargs).values_list('idTalhao'))


class PropriedadeDeleteTecnicoAPIView(DestroyAPIView):
    serializer_class = PropriedadeDetailSerializer
    lookup_field = 'idPropriedade'

    def get_queryset(self):
        return Propriedade.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.user.tipo != TECNICO:
            return Response({"error": "Um produtor não pode remover técnico da propriedade"}, status=status.HTTP_401_UNAUTHORIZED)
        if self.request.user.idUsuario != instance.tecnico.usuario_id:
            return Response({"error": "Somente o técnico que está atribuido a propriedade pode se remover"}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(instance.tecnico)
        return Response(status=status.HTTP_204_NO_CONTENT)
