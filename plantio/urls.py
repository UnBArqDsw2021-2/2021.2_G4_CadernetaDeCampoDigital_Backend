from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from plantio.views import plantio, aplicacao


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', plantio.PlantioAPIView.as_view(), name='plantio-create'),

        url(r'^(?P<pk>{})/$'.format(UUID4_URL),
            plantio.PlantioRetrieveUpdateAPIView.as_view(),
            name='plantio-detail-update'),

        url(r'^aplicar/', include([
            url(
                r'agrotoxico/$', aplicacao.AplicacaoAgrotoxicoAPIView.as_view(),
                name='plantio-associar'),
        ])),
    ]))
]
