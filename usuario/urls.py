from django.conf.urls import url
from django.urls import include

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from usuario.views.token import TokenObtainPairView


urlpatterns = [
    url(r'^login/', include([
        url(r'^$', TokenObtainPairView.as_view(), name='usuario-login'),
        url(r'^refresh/$', TokenRefreshView.as_view(), name='usuario-refresh'),
        url(r'^verify/$', TokenVerifyView.as_view(), name='usuario-verify'),
    ]))
]
