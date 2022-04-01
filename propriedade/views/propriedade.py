from plantio.models import Plantio
from plantio.serializers.plantio import PlantioSerializer

from propriedade.models import Propriedade
from propriedade.serializers.propriedade import PropriedadeSerializer

from rest_framework.generics import CreateAPIView, ListAPIView

from talhao.models import Talhao


class PropriedadeAPIView(CreateAPIView):
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        return Propriedade.objects.all()


class PropriedadeHistoricoPlantioAPIView(ListAPIView):
    serializer_class = PlantioSerializer
    lookup_field = 'idPropriedade'

    def get_queryset(self):
        return Plantio.objects.filter(
            talhao__in=Talhao.objects.filter(**self.kwargs).values_list('idTalhao'))
