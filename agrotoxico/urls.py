from django.conf.urls import url
from django.urls import include

from agrotoxico.views.tipo_agrotoxico import TipoAgrotoxicoAPIView
from agrotoxico.views.agrotoxico import AgrotoxicoAPIView
from agrotoxico.views.espera import AgrotoxicoEsperaDetailAPIView

from core.consts.urls import UUID_REGEX

urlpatterns = [
    url(r'^agrotoxico/', include([
        url(r'^$', AgrotoxicoAPIView.as_view(), name='agrotoxico-create'),
        url(r'^tipo/$', TipoAgrotoxicoAPIView.as_view(), name='tipo-agrotoxico-create'),
        url(f'^(?P<pk>{UUID_REGEX})/', include([
            url(r'^espera/cultura/$', AgrotoxicoEsperaDetailAPIView.as_view(), name='agrotoxico-espera-cultura'),
        ]))
    ]))
]
