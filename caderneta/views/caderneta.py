from rest_framework.generics import RetrieveAPIView
from caderneta.serializers.caderneta import CadernetaSerializer
from plantio.models import Plantio


class CadernetaRetrieveApiView(RetrieveAPIView):
    serializer_class = CadernetaSerializer
    lookup_field = 'idPlantio'
    queryset = Plantio.objects.all()
