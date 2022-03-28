from django.conf.urls import url
from django.urls import include

from plantio.views.plantio import PlantioAPIView


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', PlantioAPIView.as_view(), name='plantio-create'),
    ]))
]
