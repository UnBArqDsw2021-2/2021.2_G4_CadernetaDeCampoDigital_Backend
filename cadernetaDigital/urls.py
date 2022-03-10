import contextlib

from django.contrib import admin
from django.conf.urls import include, url

from django.conf import settings


url_api = []
for app in settings.LOCAL_APPS:
    # Adiciona supressão para o módulo core (testes)
    with contextlib.suppress(ModuleNotFoundError):
        url_api.append(url(r'^', include(f'{app}.urls')))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(url_api))
]
