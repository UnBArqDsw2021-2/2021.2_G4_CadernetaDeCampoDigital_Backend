from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from agrotoxico.views.tipo_agrotoxico import TipoAgrotoxicoAPIView
from agrotoxico.views.agrotoxico import AgrotoxicoAPIView, AgrotoxicoDestroyAPIView

urlpatterns = [
    url(r'^agrotoxico/', include([
        url(r'^$', AgrotoxicoAPIView.as_view(), name='agrotoxico-list-create'),

        url(
            r'^(?P<pk>{})/$'.format(UUID4_URL),
            AgrotoxicoDestroyAPIView.as_view(),
            name='agrotoxico-destroy'),

        url(r'^tipo/$', TipoAgrotoxicoAPIView.as_view(), name='tipo-agrotoxico-list-create'),
    ]))
]
