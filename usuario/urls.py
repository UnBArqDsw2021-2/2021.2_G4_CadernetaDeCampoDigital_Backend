from core.consts.urls import UUID4_URL

from django.conf.urls import url
from django.urls import include

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from usuario.views import token, usuario


urlpatterns = [
    url(r'^login/', include([
        url(r'^$', token.TokenObtainPairView.as_view(), name='usuario-login'),
        url(r'^refresh/$', TokenRefreshView.as_view(), name='usuario-refresh'),
        url(r'^verify/$', TokenVerifyView.as_view(), name='usuario-verify'),
    ])),

    url(r'^usuario/', include([
        url(
            r'^(?P<idUsuario>{})/$'.format(UUID4_URL),
            usuario.UsuarioRetrieveUpdateAPIView.as_view(),
            name='usuario-details-update'),
    ]))
]
