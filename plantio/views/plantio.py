from plantio.models import Plantio
from plantio.serializers.plantio import PlantioSerializer, PlantioListSerializer

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


class PlantioAPIView(CreateAPIView):
    serializer_class = PlantioSerializer

    def get_queryset(self):
        return Plantio.objects.all()


class PlantioRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    def get_queryset(self):
        return Plantio.objects.all()

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return PlantioListSerializer
        return PlantioSerializer
