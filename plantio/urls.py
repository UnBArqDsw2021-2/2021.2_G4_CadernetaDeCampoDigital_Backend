from django.conf.urls import url
from django.urls import include

from plantio.views.plantio import PlantioAPIView, PlantioAssociacaoAPIView


urlpatterns = [
    url(r'^plantio/', include([
        url(r'^$', PlantioAPIView.as_view(), name='plantio-create'),
        url(
            r'^(?P<idPlantio>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
            PlantioAssociacaoAPIView.as_view(), name='plantio-associar'),
    ]))
]
