from plantio.models import Plantio
from plantio.serializers.plantio import PlantioSerializer, PlantioAssociacaoSerializer

from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class PlantioAPIView(CreateAPIView):
    serializer_class = PlantioSerializer

    def get_queryset(self):
        return Plantio.objects.all()


class PlantioAssociacaoAPIView(GenericAPIView):
    lookup_field = ''
    serializer_class = PlantioAssociacaoSerializer

    def get_object(self):
        return get_object_or_404(Plantio, idPlantio=self.kwargs['idPlantio'])

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
