from cultura.serializers.espera import CulturaEsperaAgrotoxicoSerializer

from rest_framework.generics import CreateAPIView


class CulturaEsperaAgrotoxicoAPIView(CreateAPIView):
    serializer_class = CulturaEsperaAgrotoxicoSerializer
