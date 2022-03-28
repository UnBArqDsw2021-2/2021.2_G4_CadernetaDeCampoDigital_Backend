from django.conf.urls import url
from django.urls import include

from cultura.views.cultura import CulturaAPIView


urlpatterns = [
    url(r'^cultura/', include([
        url(r'^$', CulturaAPIView.as_view(), name='cultura-create'),
    ]))
]
