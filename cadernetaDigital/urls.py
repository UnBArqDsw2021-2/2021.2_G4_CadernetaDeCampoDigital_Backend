import contextlib

from django.contrib import admin
from django.conf.urls import include, url

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


url_api = []
for app in settings.LOCAL_APPS:
    # Adiciona supressão para o módulo core (testes)
    with contextlib.suppress(ModuleNotFoundError):
        url_api.append(url(r'^', include(f'{app}.urls')))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(url_api)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
