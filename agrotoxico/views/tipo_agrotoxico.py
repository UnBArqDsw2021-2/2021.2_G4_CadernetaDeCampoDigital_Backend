from agrotoxico.serializers.tipo_agrotoxico import TipoAgrotoxicoSerializer

from rest_framework.generics import CreateAPIView


class TipoAgrotoxicoAPIView(CreateAPIView):
    serializer_class = TipoAgrotoxicoSerializer
