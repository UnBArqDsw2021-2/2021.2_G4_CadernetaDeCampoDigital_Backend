from django.conf.urls import url
from django.urls import include

from tecnico.views.tecnico import TecnicoAPIView


urlpatterns = [
    url(r'^tecnico/', include([
        url(r'^$', TecnicoAPIView.as_view(), name='tecnico-create'),
    ]))
]
