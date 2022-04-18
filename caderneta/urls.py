from django.conf.urls import url
from django.urls import include
from core.consts.urls import UUID4_URL

from caderneta.views.caderneta import CadernetaRetrieveApiView

urlpatterns = [
    url(r'^caderneta/', include([
        url(r'(?P<idPlantio>{})/$'.format(UUID4_URL), CadernetaRetrieveApiView.as_view(), name="caderneta-detail")
    ]))
]
