from django.conf.urls import url
from django.urls import include

from cultura.views.cultura import CulturaListCreateAPIView
from cultura.views.espera import CulturaEsperaAgrotoxicoAPIView


urlpatterns = [
    url(r'^cultura/', include([
        url(r'^$', CulturaListCreateAPIView.as_view(), name='cultura-list-create'),
        url(r'^espera/agrotoxico/$', CulturaEsperaAgrotoxicoAPIView.as_view(), name='cultura-espera-agrotoxico')
    ]))
]
