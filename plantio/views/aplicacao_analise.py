from plantio.models import AplicacaoAgrotoxico
from plantio.serializers.aplicacao_analise import AplicacaoAgrotoxicoAnaliseSerializer

from talhao.models import Talhao
from plantio.models import Plantio

from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

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


class AplicacaoAgrotoxicoAnaliseUpdateAPIView(UpdateAPIView):
    serializer_class = AplicacaoAgrotoxicoAnaliseSerializer
    queryset = AplicacaoAgrotoxico.objects.all()
    lookup_field = 'idAplicacao'

    def update(self, request, *args, **kwargs):
        aplicacao = self.get_object()

        invalid = self.is_user_invalid(self.request.user, aplicacao)
        if invalid:
            return Response(*invalid)

        return super().update(request, *args, **kwargs)

    def is_user_invalid(self, user, aplicacao):
        if user.is_anonymous or user.tipo != TECNICO:
            return ({"error": "Acesso negado"}, status.HTTP_403_FORBIDDEN)

        tecnico_aplicacao = aplicacao.propriedade.tecnico

        if not tecnico_aplicacao:
            return ({"error": "A propriedade onde ocorreu a aplicação não tem um tecnico supervisor"}, status.HTTP_400_BAD_REQUEST)

        if tecnico_aplicacao.usuario != user:
            return ({"error": "Você não supervisiona a propriedade dessa aplicacao"}, status.HTTP_401_UNAUTHORIZED)
