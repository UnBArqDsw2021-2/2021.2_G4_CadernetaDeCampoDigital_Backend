from plantio.models import Plantio
from plantio.serializers.plantio import PlantioSerializer

from rest_framework.generics import CreateAPIView


class PlantioAPIView(CreateAPIView):
    serializer_class = PlantioSerializer

    def get_queryset(self):
        return Plantio.objects.all()
