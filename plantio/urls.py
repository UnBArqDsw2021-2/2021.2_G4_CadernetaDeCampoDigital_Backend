from django.conf.urls import url
from django.urls import include

from plantio.views.plantio import PlantioAPIView
from plantio.views.aplicacao import AplicacaoAgrotoxicoAPIView


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', PlantioAPIView.as_view(), name='plantio-create'),

        url(r'^aplicar/', include([
            url(
                r'agrotoxico/$', AplicacaoAgrotoxicoAPIView.as_view(),
                name='plantio-associar'),
        ])),
    ]))
]
