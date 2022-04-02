from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from propriedade.views.propriedade import PropriedadeAPIView, PropriedadeRetrieveAPIView


urlpatterns = [
    url(r'^propriedade/', include([
        url(r'^$', PropriedadeAPIView.as_view(), name='propriedade-create-list'),
        url(
            r'^(?P<pk>{})/$'.format(UUID4_URL),
            PropriedadeRetrieveAPIView.as_view(),
            name='propriedade-detail'
        ),
    ]))
]
