from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from core.consts.urls import UUID4_URL
from plantio.views import plantio, aplicacao, aplicacao_analise


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', plantio.PlantioAPIView.as_view(), name='plantio-create'),

        url(r'^(?P<pk>{})/$'.format(UUID4_URL),
            plantio.PlantioRetrieveUpdateAPIView.as_view(),
            name='plantio-detail-update'),

        url(r'^aplicar/', include([
            url(
                r'agrotoxico/$', aplicacao.AplicacaoAgrotoxicoCreateAPIView.as_view(),
                name='plantio-associar'),
        ])),

        url(r'^analise/agrotoxico/', include([
            url(r'^$', aplicacao_analise.AplicacaoAgrotoxicoAnaliseApiView.as_view(), name="plantio-analise-aplicacao-agrotoxico"),
            url(r'(?P<idAplicacao>{})/$'.format(UUID4_URL), aplicacao_analise.AplicacaoAgrotoxicoAnaliseUpdateAPIView.as_view(), name="plantio-analise-aplicacao-agrotoxico-update"),
        ])),
    ]))
]
