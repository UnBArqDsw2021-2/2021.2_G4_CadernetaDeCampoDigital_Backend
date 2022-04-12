from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from talhao.views.talhao import TalhaoAPIView, TalhaoDetailAPIView


urlpatterns = [
    url(r'^talhao/', include([
        url(r'^$', TalhaoAPIView.as_view(), name='talhao-create'),

        url(
            r'^(?P<idTalhao>{})/historico/plantio/$'.format(UUID4_URL),
            TalhaoDetailAPIView.as_view(),
            name='talhao-historico-plantio'
        )
    ]))
]
