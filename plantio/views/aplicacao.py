from plantio.models import AplicacaoAgrotoxico
from plantio.serializers.aplicacao import AplicacaoAgrotoxicoSerializer

from talhao.models import Talhao
from plantio.models import Plantio

from rest_framework.generics import ListCreateAPIView

from core.consts.usuarios import TECNICO


class AplicacaoAgrotoxicoListCreateAPIView(ListCreateAPIView):
    serializer_class = AplicacaoAgrotoxicoSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            breakpoint()
            return AplicacaoAgrotoxico.objects.none()

        if user.tipo == TECNICO:
            propriedades = user.tecnico.propriedade_set
        else:
            propriedades = user.produtor.propriedade_set

        talhoes = Talhao.objects.filter(idPropriedade__in=propriedades.all())
        plantios = Plantio.objects.filter(talhao__in=talhoes.all())

        return AplicacaoAgrotoxico.objects.filter(plantio__in=plantios).all()
