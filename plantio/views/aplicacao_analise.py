from plantio.models import AplicacaoAgrotoxico
from plantio.serializers.aplicacao_analise import AplicacaoAgrotoxicoAnaliseSerializer

from talhao.models import Talhao
from plantio.models import Plantio

from rest_framework.generics import ListAPIView

from core.consts.usuarios import TECNICO


class AplicacaoAgrotoxicoAnaliseApiView(ListAPIView):
    serializer_class = AplicacaoAgrotoxicoAnaliseSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return AplicacaoAgrotoxico.objects.none()

        if user.tipo == TECNICO:
            propriedades = user.tecnico.propriedade_set
        else:
            propriedades = user.produtor.propriedade_set

        talhoes = Talhao.objects.filter(idPropriedade__in=propriedades.all())
        plantios = Plantio.objects.filter(talhao__in=talhoes.all())

        return AplicacaoAgrotoxico.objects.filter(plantio__in=plantios).all()
