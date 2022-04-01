from django.conf.urls import url
from django.urls import include

from agrotoxico.views.tipo_agrotoxico import TipoAgrotoxicoAPIView
from agrotoxico.views.agrotoxico import AgrotoxicoAPIView
from agrotoxico.views.espera import AgrotoxicoEsperaAPIView

urlpatterns = [
    url(r'^agrotoxico/', include([
        url(r'^$', AgrotoxicoAPIView.as_view(), name='agrotoxico-create'),
        url(r'^tipo/$', TipoAgrotoxicoAPIView.as_view(), name='tipo-agrotoxico-create'),
        url(f'^espera/cultura/$', AgrotoxicoEsperaAPIView.as_view(), name='agrotoxico-espera-cultura')
    ]))
]
