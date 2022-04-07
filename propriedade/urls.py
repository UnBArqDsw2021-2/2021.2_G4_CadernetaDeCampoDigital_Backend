from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from propriedade.views.propriedade import PropriedadeAPIView, PropriedadeHistoricoPlantioAPIView, PropriedadeRetrieveAPIView, PropriedadeDeleteTecnicoAPIView


urlpatterns = [
    url(r'^propriedade/', include([
        url(r'^$', PropriedadeAPIView.as_view(), name='propriedade-create-list'),

        url(
            r'^(?P<pk>{})/$'.format(UUID4_URL),
            PropriedadeRetrieveAPIView.as_view(),
            name='propriedade-detail'),

        url(
            r'(?P<idPropriedade>{})/historico/plantio/$'.format(UUID4_URL),
            PropriedadeHistoricoPlantioAPIView.as_view(),
            name='propriedade-historico-plantio'),

        url(
            r'(?P<idPropriedade>{})/tecnico/$'.format(UUID4_URL),
            PropriedadeDeleteTecnicoAPIView.as_view(),
            name='propriedade-delete-tecnico'),
    ]))
]
