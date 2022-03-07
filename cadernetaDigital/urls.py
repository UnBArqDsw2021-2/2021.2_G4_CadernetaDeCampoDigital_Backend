from django.contrib import admin
from django.conf.urls import include, url

from django.conf import settings

from catalogo import urls


url_api = []
for app in settings.LOCAL_APPS:
    url_api.append(url(r'^', include(f'{app}.urls')))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(url_api))
]
