from agrotoxico.models import TipoAgrotoxico
from agrotoxico.serializers.tipo_agrotoxico import TipoAgrotoxicoSerializer

from rest_framework.generics import ListCreateAPIView


class TipoAgrotoxicoAPIView(ListCreateAPIView):
    queryset = TipoAgrotoxico.objects.all()
    serializer_class = TipoAgrotoxicoSerializer
