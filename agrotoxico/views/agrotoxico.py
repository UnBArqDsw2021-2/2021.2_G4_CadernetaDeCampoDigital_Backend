from agrotoxico.models import Agrotoxico
from agrotoxico.serializers.agrotoxico import AgrotoxicoCreateSerializer, AgrotoxicoListSerializer

from rest_framework.generics import ListCreateAPIView


class AgrotoxicoAPIView(ListCreateAPIView):
    queryset = Agrotoxico.objects.all()

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return AgrotoxicoListSerializer
        return AgrotoxicoCreateSerializer
