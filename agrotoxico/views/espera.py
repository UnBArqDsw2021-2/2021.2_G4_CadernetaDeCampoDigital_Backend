from agrotoxico.serializers.espera import AgrotoxicoEsperaSerializer

from rest_framework.generics import CreateAPIView


class AgrotoxicoEsperaAPIView(CreateAPIView):
    serializer_class = AgrotoxicoEsperaSerializer
