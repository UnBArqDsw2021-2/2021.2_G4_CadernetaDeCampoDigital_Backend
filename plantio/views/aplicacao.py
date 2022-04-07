from plantio.serializers.aplicacao import AplicacaoAgrotoxicoSerializer

from rest_framework.generics import CreateAPIView


class AplicacaoAgrotoxicoCreateAPIView(CreateAPIView):
    serializer_class = AplicacaoAgrotoxicoSerializer
