from agrotoxico.serializers.agrotoxico import AgrotoxicoSerializer

from rest_framework.generics import CreateAPIView


class AgrotoxicoAPIView(CreateAPIView):
    serializer_class = AgrotoxicoSerializer
