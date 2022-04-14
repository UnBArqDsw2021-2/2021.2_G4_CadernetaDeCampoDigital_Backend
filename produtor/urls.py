from django.conf.urls import url
from django.urls import include

from produtor.views.produtor import ProdutorAPIView


urlpatterns = [
    url(r'^produtor/', include([
        url(r'^$', ProdutorAPIView.as_view(), name='produtor-create'),
    ]))
]
