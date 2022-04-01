from django.conf.urls import url
from django.urls import include

from plantio.views import plantio, aplicacao


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', plantio.PlantioAPIView.as_view(), name='plantio-create'),

        url(r'^aplicar/', include([
            url(
                r'agrotoxico/$', aplicacao.AplicacaoAgrotoxicoAPIView.as_view(),
                name='plantio-associar'),
        ])),

        url(r'^(?P<idPropriedade>[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab][0-9A-Za-z]{3}-[0-9A-Za-z]{12})/historico/', include([
            url(
                r'^propriedade/$', plantio.PlantioHistoricoPropriedadeAPIView.as_view(),
                name='plantio-historico-propriedade'),
        ])),
    ]))
]
