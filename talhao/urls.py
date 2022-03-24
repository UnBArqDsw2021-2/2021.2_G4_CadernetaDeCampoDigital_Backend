from django.conf.urls import url
from django.urls import include

from talhao.views.talhao import TalhaoAPIView


urlpatterns = [
    url(r'^talhao/', include([
        url(r'^$', TalhaoAPIView.as_view(), name='talhao-create')
    ]))
]
