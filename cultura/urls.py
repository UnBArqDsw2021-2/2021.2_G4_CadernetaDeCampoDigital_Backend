from django.conf.urls import url
from django.urls import include

from cultura.views.cultura import CulturaAPIView
from cultura.views.espera import CulturaEsperaAgrotoxicoAPIView


urlpatterns = [
    url(r'^cultura/', include([
        url(r'^$', CulturaAPIView.as_view(), name='cultura-create'),
        url(f'^espera/agrotoxico/$', CulturaEsperaAgrotoxicoAPIView.as_view(), name='cultura-espera-agrotoxico')
    ]))
]
