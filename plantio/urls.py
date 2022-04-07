from django.conf.urls import url
from django.urls import include

from plantio.views import plantio, aplicacao, aplicacao_analise


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', plantio.PlantioAPIView.as_view(), name='plantio-create'),

        url(r'^aplicar/', include([
            url(
                r'agrotoxico/$', aplicacao.AplicacaoAgrotoxicoCreateAPIView.as_view(),
                name='plantio-associar'),
        ])),

        url(r'^analise/', include([
            url(
                r'agrotoxico/$', aplicacao_analise.AplicacaoAgrotoxicoAnaliseApiView.as_view(),
                name="plantio-analise-aplicacao-agrotoxico"),
        ])),
    ]))
]
