from agrotoxico.models import Agrotoxico
from agrotoxico.serializers.agrotoxico import AgrotoxicoCreateSerializer, AgrotoxicoListSerializer

from rest_framework.generics import ListCreateAPIView


class AgrotoxicoAPIView(ListCreateAPIView):
    queryset = Agrotoxico.objects.all()
    write_serializer_class = AgrotoxicoCreateSerializer
    read_serializer_class = AgrotoxicoListSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.read_serializer_class
        return self.write_serializer_class
