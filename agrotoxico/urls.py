from django.conf.urls import url
from django.urls import include

from agrotoxico.views.tipo_agrotoxico import TipoAgrotoxicoAPIView


urlpatterns = [
    url(r'^agrotoxico/', include([
        url(r'^tipo$', TipoAgrotoxicoAPIView.as_view(), name='tipo-agrotoxico-create'),
    ]))
]
