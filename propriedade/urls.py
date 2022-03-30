from django.conf.urls import url
from django.urls import include

from propriedade.views.propriedade import PropriedadeAPIView, PropriedadeRetrieveAPIViewTest


urlpatterns = [
    url(r'^propriedade/', include([
        url(r'^$', PropriedadeAPIView.as_view(), name='propriedade-create-list'),
        url(r'^(?P<pk>[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab][0-9A-Za-z]{3}-[0-9A-Za-z]{12})/$', PropriedadeRetrieveAPIViewTest.as_view(), name='propriedade-detail'),
    ]))
]
