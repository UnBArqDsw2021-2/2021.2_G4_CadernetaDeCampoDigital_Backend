from plantio.models import Plantio
from plantio.serializers.plantio import PlantioSerializer

from rest_framework.generics import CreateAPIView, ListAPIView

from talhao.models import Talhao


class PlantioAPIView(CreateAPIView):
    serializer_class = PlantioSerializer

    def get_queryset(self):
        return Plantio.objects.all()


class PlantioHistoricoPropriedadeAPIView(ListAPIView):
    serializer_class = PlantioSerializer
    lookup_field = 'idPropriedade'

    def get_queryset(self):
        return Plantio.objects.filter(
            talhao__in=Talhao.objects.filter(**self.kwargs).values_list('idTalhao'))
