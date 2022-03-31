from plantio.models import AplicacaoAgrotoxico
from plantio.serializers.aplicacao import AplicacaoAgrotoxicoSerializer

from rest_framework.generics import CreateAPIView


class AplicacaoAgrotoxicoAPIView(CreateAPIView):
    serializer_class = AplicacaoAgrotoxicoSerializer

    def get_queryset(self):
        return AplicacaoAgrotoxico.objects.all()
