from django.conf.urls import url
from django.urls import include

from propriedade.views.propriedade import PropriedadeAPIView


urlpatterns = [
    url(r'^propriedade/', include([
        url(r'^$', PropriedadeAPIView.as_view(), name='propriedade-create-list'),
    ]))
]
