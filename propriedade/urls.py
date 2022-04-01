from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from propriedade.views.propriedade import PropriedadeAPIView, PropriedadeHistoricoPlantioAPIView


urlpatterns = [
    url(r'^propriedade/', include([
        url(r'^$', PropriedadeAPIView.as_view(), name='propriedade-create'),

        url(
            r'(?P<idPropriedade>{})/historico/plantio/$'.format(UUID4_URL),
                PropriedadeHistoricoPlantioAPIView.as_view(),
                name='propriedade-historico-plantio'),
    ]))
]
